from decimal import Decimal

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import CadastroForm, OrcamentoForm
from .models import Compra, Pacote
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
        qtd = dados[str(p.pk)]
        subtotal = p.preco * qtd
        total += subtotal
        itens.append({"pacote": p, "quantidade": qtd, "subtotal": subtotal})
    return itens, total


def pacotes(request):
    itens, total = _carrinho(request)
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
    for item in itens:
        original = item["subtotal"]
        Compra.objects.create(
            usuario=request.user, pacote=item["pacote"], destino=item["pacote"].nome,
            quantidade=item["quantidade"], valor_original=original,
            desconto_percentual=desconto,
            valor_final=original - original * desconto / 100,
        )
    request.session["carrinho"] = {}
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
