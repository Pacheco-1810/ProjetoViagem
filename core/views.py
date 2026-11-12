from decimal import Decimal
from functools import wraps

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.db.models import Q, Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST

from .forms import (
    AdicionarCarrinhoForm,
    CadastroForm,
    FiltroPacoteForm,
    HotelForm,
    OrcamentoForm,
    PacoteForm,
)
from .models import Compra, Hotel, Pacote
from .services import MAX_VIAJANTES, calcular_nivel, criar_reserva, desconto_do_usuario


def staff_required(view):
    """Só administradores (is_staff) acessam. Os outros recebem erro 403."""

    @login_required
    @wraps(view)
    def interna(request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied
        return view(request, *args, **kwargs)

    return interna


def erros_do_form(form):
    erros = []
    for campo, lista in form.errors.items():
        rotulo = form.fields[campo].label if campo in form.fields else ""
        for erro in lista:
            erros.append(f"{rotulo}: {erro}" if rotulo else str(erro))
    return " ".join(erros)


# ---------- páginas públicas ----------

def index(request):
    slides = Pacote.objects.filter(ativo=True, no_carrossel=True)
    return render(request, "index.html", {"slides": slides})


def sobre(request):
    return render(request, "sobre.html")


def contato(request):
    form = OrcamentoForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Mensagem enviada com sucesso! Em breve entraremos em contato.")
        return redirect("contato")
    return render(request, "contato.html", {"form": form})


def cadastro(request):
    if request.user.is_authenticated:
        return redirect("pacotes")

    form = CadastroForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        login(request, form.save())
        messages.success(request, "Cadastro realizado com sucesso!")
        return redirect("pacotes")
    return render(request, "cadastro.html", {"form": form})


# ---------- pacotes e carrinho ----------
# O carrinho fica na sessão: {"<id do pacote>": {"qtd": 2, "hotel": <id do hotel>}}

def obter_carrinho(request):
    carrinho = request.session.get("carrinho", {})
    itens = []
    total = Decimal("0.00")

    for pacote in Pacote.objects.filter(pk__in=carrinho.keys(), ativo=True):
        dados = carrinho[str(pacote.pk)]
        hotel = Hotel.objects.filter(pk=dados["hotel"], pacote=pacote).first()
        preco = pacote.preco + (hotel.acrescimo if hotel else 0)
        subtotal = preco * dados["qtd"]
        total += subtotal
        itens.append({"pacote": pacote, "quantidade": dados["qtd"], "hotel": hotel, "subtotal": subtotal})

    return itens, total


def pacotes(request):
    filtro = FiltroPacoteForm(request.GET or None)
    lista = Pacote.objects.filter(ativo=True).prefetch_related("hoteis")
    so_disponiveis = False

    if filtro.is_valid():
        dados = filtro.cleaned_data
        if dados["q"]:
            lista = lista.filter(Q(nome__icontains=dados["q"]) | Q(descricao__icontains=dados["q"]))
        if dados["preco_max"] is not None:
            lista = lista.filter(preco__lte=dados["preco_max"])
        so_disponiveis = dados["so_disponiveis"]
    elif filtro.is_bound:
        messages.error(request, erros_do_form(filtro))

    lista = list(lista)
    if so_disponiveis:
        lista = [p for p in lista if p.tem_vagas()]

    itens, total = obter_carrinho(request)
    contexto = {"pacotes": lista, "itens": itens, "total": total, "filtro": filtro}
    return render(request, "pacotes.html", contexto)


@login_required
@require_POST
def adicionar_carrinho(request, pk):
    pacote = get_object_or_404(Pacote, pk=pk, ativo=True)
    form = AdicionarCarrinhoForm(request.POST, pacote=pacote)

    if not form.is_valid():
        messages.error(request, erros_do_form(form))
        return redirect("pacotes")

    carrinho = request.session.get("carrinho", {})
    quantidade = carrinho.get(str(pacote.pk), {}).get("qtd", 0) + form.cleaned_data["quantidade"]

    if quantidade > MAX_VIAJANTES:
        messages.error(request, f"O limite é de {MAX_VIAJANTES} viajantes por pacote.")
        return redirect("pacotes")

    hoteis = list(pacote.hoteis.all())
    if not hoteis:
        messages.error(request, "Este pacote ainda não possui hotéis cadastrados.")
        return redirect("pacotes")

    hotel = form.cleaned_data["hotel"] or max(hoteis, key=lambda h: h.disponiveis())

    if hotel.disponiveis() < quantidade:
        messages.error(request, f"{hotel.nome} possui apenas {hotel.disponiveis()} vaga(s) disponíveis.")
        return redirect("pacotes")

    carrinho[str(pacote.pk)] = {"qtd": quantidade, "hotel": hotel.pk}
    request.session["carrinho"] = carrinho
    messages.success(request, "Pacote adicionado ao carrinho!")
    return redirect("pacotes")


@require_POST
def remover_carrinho(request, pk):
    carrinho = request.session.get("carrinho", {})
    carrinho.pop(str(pk), None)
    request.session["carrinho"] = carrinho
    messages.success(request, "Item removido do carrinho.")
    return redirect("pacotes")


@login_required
@require_POST
def finalizar_compra(request):
    itens, total = obter_carrinho(request)

    if not itens:
        messages.warning(request, "Adicione pelo menos um pacote ao carrinho.")
        return redirect("pacotes")

    # o desconto é calculado uma vez, antes de criar as reservas do carrinho
    desconto = desconto_do_usuario(request.user)

    try:
        with transaction.atomic():
            for item in itens:
                criar_reserva(request.user, item["pacote"], item["quantidade"], item["hotel"], desconto)
    except ValueError as erro:
        messages.error(request, f"Não foi possível finalizar a reserva: {erro}")
        return redirect("pacotes")

    request.session["carrinho"] = {}
    messages.success(request, f"Reserva confirmada! Desconto aplicado: {desconto}%.")
    return redirect("perfil")


# ---------- perfil e reservas do cliente ----------

@login_required
def perfil(request):
    reservas = request.user.compras.order_by("-data")
    confirmadas = reservas.filter(status=Compra.CONFIRMADA)
    total_gasto = confirmadas.aggregate(total=Sum("valor_final"))["total"] or Decimal("0.00")

    contexto = {
        "compras": reservas,
        "qtd": confirmadas.count(),
        "total_gasto": total_gasto,
        "n": calcular_nivel(confirmadas.count()),
    }
    return render(request, "perfil.html", contexto)


@login_required
@require_POST
def cancelar_reserva(request, pk):
    # filtrar por usuario impede cancelar a reserva de outra pessoa (retorna 404)
    reserva = get_object_or_404(Compra, pk=pk, usuario=request.user)

    try:
        reserva.cancelar()
        messages.success(request, f"Reserva de {reserva.destino} cancelada. As vagas foram liberadas.")
    except ValueError as erro:
        messages.warning(request, str(erro))

    return redirect("perfil")


# ---------- gestão (administrador) ----------

@staff_required
def gestao_pacotes(request):
    busca = request.GET.get("q", "").strip()
    lista = Pacote.objects.all()

    if busca:
        lista = lista.filter(Q(nome__icontains=busca) | Q(descricao__icontains=busca))

    return render(request, "gestao_pacotes.html", {"pacotes": lista, "busca": busca})


@staff_required
def gestao_pacote_form(request, pk=None):
    pacote = get_object_or_404(Pacote, pk=pk) if pk else None
    form = PacoteForm(request.POST or None, request.FILES or None, instance=pacote)

    if request.method == "POST" and form.is_valid():
        salvo = form.save()
        if pacote is None:
            messages.success(request, "Pacote criado! Agora cadastre os hotéis e as vagas.")
            return redirect("gestao_pacote_editar", pk=salvo.pk)
        messages.success(request, "Pacote atualizado com sucesso.")
        return redirect("gestao_pacotes")

    contexto = {"form": form, "pacote": pacote, "titulo": "Editar pacote" if pacote else "Novo pacote"}
    return render(request, "gestao_pacote_form.html", contexto)


@staff_required
def gestao_pacote_excluir(request, pk):
    pacote = get_object_or_404(Pacote, pk=pk)
    ativas = Compra.objects.filter(pacote=pacote, status=Compra.CONFIRMADA).count()

    if ativas:
        messages.error(
            request, f"Existem {ativas} reserva(s) confirmada(s). Desative o pacote em vez de excluí-lo."
        )
        return redirect("gestao_pacotes")

    if request.method == "POST":
        pacote.delete()
        messages.success(request, "Pacote excluído com sucesso.")
        return redirect("gestao_pacotes")

    contexto = {
        "objeto": pacote,
        "voltar": reverse("gestao_pacotes"),
        "aviso": "Os hotéis deste pacote também serão excluídos.",
    }
    return render(request, "gestao_excluir.html", contexto)


@staff_required
def gestao_hotel_form(request, pacote_pk=None, pk=None):
    if pk:
        hotel = get_object_or_404(Hotel, pk=pk)
    else:
        hotel = Hotel(pacote=get_object_or_404(Pacote, pk=pacote_pk))

    form = HotelForm(request.POST or None, instance=hotel)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Hotel salvo com sucesso.")
        return redirect("gestao_pacote_editar", pk=hotel.pacote_id)

    contexto = {
        "form": form,
        "voltar": reverse("gestao_pacote_editar", args=[hotel.pacote_id]),
        "titulo": f"{'Editar' if pk else 'Novo'} hotel - {hotel.pacote.nome}",
    }
    return render(request, "gestao_form.html", contexto)


@staff_required
def gestao_hotel_excluir(request, pk):
    hotel = get_object_or_404(Hotel, pk=pk)
    voltar = reverse("gestao_pacote_editar", args=[hotel.pacote_id])

    if hotel.ocupadas() > 0:
        messages.error(
            request,
            f"{hotel.nome} possui {hotel.ocupadas()} vaga(s) reservadas. Cancele as reservas antes de excluir.",
        )
        return redirect(voltar)

    if request.method == "POST":
        hotel.delete()
        messages.success(request, "Hotel excluído com sucesso.")
        return redirect(voltar)

    return render(request, "gestao_excluir.html", {"objeto": hotel, "voltar": voltar})


@staff_required
def gestao_reservas(request):
    lista = Compra.objects.select_related("usuario", "pacote", "hotel").order_by("-data")
    status = request.GET.get("status", "")
    busca = request.GET.get("q", "").strip()

    if status in (Compra.CONFIRMADA, Compra.CANCELADA):
        lista = lista.filter(status=status)

    if busca:
        lista = lista.filter(Q(usuario__email__icontains=busca) | Q(destino__icontains=busca))

    return render(request, "gestao_reservas.html", {"reservas": lista, "status": status, "busca": busca})
