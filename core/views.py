from decimal import Decimal
from collections import defaultdict

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import CadastroForm, OrcamentoForm
from .models import Compra, Pacote, Hotel
from .niveis import calcular_desconto, calcular_nivel


def index(request):
    slides = Pacote.objects.filter(ativo=True, no_carrossel=True)
    return render(request, "core/index.html", {"slides": slides})


def sobre(request):
    return render(request, "core/sobre.html")


def contato(request):
    form = OrcamentoForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Mensagem enviada com sucesso! Em breve entraremos em contato.")
        return redirect("contato")
    return render(request, "core/contato.html", {"form": form})


def cadastro(request):
    form = CadastroForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        login(request, form.save())
        messages.success(request, "Cadastro realizado com sucesso!")
        return redirect("pacotes")
    return render(request, "registration/cadastro.html", {"form": form})


# ---------- Carrinho (guardado na sessão) ----------

def _carrinho(request):
    dados = request.session.get("carrinho", {})
    pacotes = Pacote.objects.filter(pk__in=dados.keys(), ativo=True)
    itens, total = [], Decimal("0")
    for p in pacotes:
        item = _item(dados[str(p.pk)])
        hotel = None
        if item["hotel"]:
            hotel = Hotel.objects.filter(pk=item["hotel"],pacote=p).first()
        qtd = dados[str(p.pk)]
        subtotal = p.preco * qtd
        total += subtotal
        itens.append({"pacote": p, "quantidade": qtd, "subtotal": subtotal,"hotel": hotel})
    return itens, total


def pacotes(request):
    itens, total = _carrinho(request)
    lista = list(Pacote.objects.filter(ativo=True))
    por_pacote = _hoteis_por_pacote()
    for p in lista:
        p.lista_hoteis = por_pacote.get(p.pk,[])
        p.esgotado = bool(p.lista_hoteis) and all (h.livres <= 0 for h in p.lista_hoteis)
    return render(request, "core/pacotes.html", {
        "pacotes": Pacote.objects.filter(ativo=True),
        "itens": itens, "total": total,
    })


@require_POST
def adicionar_carrinho(request, pk):
    if not request.user.is_authenticated:
        messages.warning(request, "Você precisa realizar login para adicionar itens ao carrinho.")
        return redirect("login")
    pacote = get_object_or_404(Pacote, pk=pk, ativo=True)
    try:
        qtd = max(1, int(request.POST.get("quantidade", 1)))
    except ValueError:
        qtd = 1
    carrinho = request.session.get("carrinho", {})
    atual = _item(carrinho.get(str(pacote.pk),{"qtd":0 , "hotel": None}))
    qtd_total = atual ["qtd"] + qtd

    hotel_id = None
    hoteis = _hoteis_por_pacote().get(pacote.pk,[])
    if hoteis:
        escolhido = request.POST.get("hotel","")
        if escolhido: #hotel escolhido pelo clente
            hotel = next((h for h in hoteis if str(h.pk) == escolhido), None)
            if hotel is None:
                messages.error(request,"Hotel inválido.")
                return redirect("pacotes")
            if hotel.livres < qtd_total:
                messages.error(request,f"{hotel.nome} tem só {hotel.livres} vaga(s).")
                return redirect("pacotes")
            hotel_id = hotel.pk
        elif max(h.livres for h in hoteis) < qtd_total:
            messages.error(request, "Não há vagas de suficientes nesse pacotes.")
            return redirect("pacotes")

    carrinho[str(pacote.pk)] = carrinho.get(str(pacote.pk), 0) + qtd
    request.session["carrinho"] = carrinho
    return redirect("pacotes")


@require_POST
def remover_carrinho(request, pk):
    carrinho = request.session.get("carrinho", {})
    carrinho.pop(str(pk), None)
    request.session["carrinho"] = carrinho
    return redirect("pacotes")


@login_required
@require_POST
def finalizar_compra(request):
    itens, total = _carrinho(request)
    if not itens:
        messages.warning(request, "Adicione pelo menos um pacote ao carrinho antes de finalizar.")
        return redirect("pacotes")

    desconto = calcular_desconto(request.user.compras.count())
    try:
        with transaction.atomic():
            for item in itens:
                pacote, qtd = item["pacote"], item["quantidade"]

                hoteis = list(Hotel.objects.select_for_update()
                              .filter(pacote=pacote).order_by("pk"))
                hotel = None
                if hoteis:
                    ocup = dict(Compra.objects.filter(hotel__in=hoteis)
                                .values("hotel").annotate(t=Sum("quantidade"))
                                .values_list("hotel", "t"))
                    livres = {h.pk: h.vagas - (ocup.get(h.pk) or 0) for h in hoteis}

                    escolhido = item["hotel"].pk if item["hotel"] else None
                    if escolhido in livres:
                        hotel = next(h for h in hoteis if h.pk == escolhido)
                    else:
                        hotel = max(hoteis, key=lambda h: livres[h.pk])
                    if livres[hotel.pk] < qtd:
                        raise SemVaga(hotel.nome)

                preco = pacote.preco + (hotel.acrescimo if hotel else 0)
                original = preco * qtd
                Compra.objects.create(
                    usuario=request.user, pacote=pacote, destino=pacote.nome,
                    hotel=hotel, hotel_nome=hotel.nome if hotel else "",
                    quantidade=qtd, valor_original=original,
                    desconto_percentual=desconto,
                    valor_final=original - original * desconto / 100,
                )
    except SemVaga as e:
        messages.success(request, f"Compra finalizada com sucesso! Desconto aplicado: {desconto}%")
        return redirect("perfil")


@login_required
def perfil(request):
    compras = request.user.compras.all()
    qtd = compras.count()
    total = compras.aggregate(t=Sum("valor_final"))["t"] or 0
    return render(request, "core/perfil.html", {
        "compras": compras, "qtd": qtd, "total_gasto": total, "n": calcular_nivel(qtd),
    })

class SemVaga(Exception):
    pass

def _item(valor):
    """Aceita o formato antigo (só a quantidade) e o novo (dict)."""
    if isinstance(valor,dict):
        return {"qtd": valor.get("qtd",1), "hotel": valor.get("hotel")}
    return {"qtd": valor, "hotel": None}

def _hoteis_por_pacote():
    """Hotéis com vagas livres calculadas, agrupados por pacote."""
    hoteis = Hotel.objects.annotate(ocup=Coalesce(Sum("compras__quantidade"), 0))
    por_pacote = defaultdict(list)
    for h in hoteis:
        h.livres = h.vagas - h.ocup
        por_pacote[h.pacote_id].append(h)
    return por_pacote




