
from collections import defaultdict
from decimal import Decimal
from functools import wraps

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
<<<<<<< HEAD
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.db.models import Q, Sum
=======
from django.core.exceptions import PermissionDenied, ValidationError
from django.db import transaction
from django.db.models import Q, Sum
from django.db.models.functions import Coalesce
>>>>>>> 1c8228b5a3fb9d6ec982ed510696cfa6d2fb7eb7
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST

from .forms import (
<<<<<<< HEAD
    AdicionarCarrinhoForm,
    CadastroForm,
    FiltroPacoteForm,
    HotelForm,
    OrcamentoForm,
    PacoteForm,
)
from .models import Compra, Hotel, Pacote
from .services import MAX_VIAJANTES, calcular_nivel, criar_reserva, desconto_do_usuario
=======
    CadastroForm,
    OrcamentoForm,
    AdicionarCarrinhoForm,
    FiltroPacoteForm,
    HotelForm,
    PacoteForm,
)
>>>>>>> 1c8228b5a3fb9d6ec982ed510696cfa6d2fb7eb7

from .models import Compra, Pacote, Hotel
from .niveis import calcular_nivel
from .services import MAX_VIAJANTES, criar_reserva


# =====================================================
# PERMISSÕES
# =====================================================

def staff_required(view):
    """Permite acesso somente a administradores."""

    @login_required
    @wraps(view)
    def interna(request, *args, **kwargs):

        if not request.user.is_staff:
            raise PermissionDenied

        return view(request, *args, **kwargs)

    return interna


def resumo_erros(form):
    """Organiza as mensagens de erro dos formulários."""

    partes = []

    for campo, erros in form.errors.items():

        rotulo = (
            form.fields[campo].label
            if campo in form.fields
            else ""
        )

        for erro in erros:

            if rotulo:
                partes.append(f"{rotulo}: {erro}")
            else:
                partes.append(str(erro))

    return " ".join(partes)


# =====================================================
# PÁGINAS PÚBLICAS
# =====================================================

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
<<<<<<< HEAD
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
=======

    slides = Pacote.objects.filter(
        ativo=True,
        no_carrossel=True
    )

    return render(
        request,
        "core/index.html",
        {"slides": slides}
    )


def sobre(request):

    return render(
        request,
        "core/sobre.html"
    )


def contato(request):
>>>>>>> 1c8228b5a3fb9d6ec982ed510696cfa6d2fb7eb7

    form = OrcamentoForm(request.POST or None)

    if request.method == "POST" and form.is_valid():

        form.save()

        messages.success(
            request,
            "Mensagem enviada com sucesso! Em breve entraremos em contato."
        )

        return redirect("contato")

    return render(
        request,
        "core/contato.html",
        {"form": form}
    )


# =====================================================
# CADASTRO DE CLIENTES
# =====================================================

def cadastro(request):
<<<<<<< HEAD
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
=======

    if request.user.is_authenticated:
        return redirect("pacotes")

    form = CadastroForm(request.POST or None)

    if request.method == "POST" and form.is_valid():

        usuario = form.save()

        login(request, usuario)

        messages.success(
            request,
            "Cadastro realizado com sucesso!"
        )

        return redirect("pacotes")

    return render(
        request,
        "registration/cadastro.html",
        {"form": form}
    )


# =====================================================
# CARRINHO DE COMPRAS
# =====================================================

def item_carrinho(valor):
    """Compatibilidade com carrinhos antigos e novos."""

    if isinstance(valor, dict):

        return {
            "qtd": valor.get("qtd", 1),
            "hotel": valor.get("hotel")
        }

    return {
        "qtd": valor,
        "hotel": None
    }


def hoteis_por_pacote():
    """Calcula a ocupação considerando apenas reservas confirmadas."""

    ocupadas = Sum(
        "compras__quantidade",
        filter=Q(compras__status=Compra.CONFIRMADA)
    )

    hoteis = Hotel.objects.annotate(
        ocup=Coalesce(ocupadas, 0)
    )

    resultado = defaultdict(list)

    for hotel in hoteis:

        hotel.livres = max(
            hotel.vagas - hotel.ocup,
            0
        )

        resultado[hotel.pacote_id].append(hotel)

    return resultado


def obter_carrinho(request):

    dados = request.session.get("carrinho", {})

    pacotes = Pacote.objects.filter(
        pk__in=dados.keys(),
        ativo=True
    )

    itens = []
    total = Decimal("0.00")

    for pacote in pacotes:

        item = item_carrinho(
            dados[str(pacote.pk)]
        )

        hotel = None

        if item["hotel"]:

            hotel = Hotel.objects.filter(
                pk=item["hotel"],
                pacote=pacote
            ).first()

        preco = pacote.preco

        if hotel:
            preco += hotel.acrescimo

        subtotal = preco * item["qtd"]

        total += subtotal

        itens.append({
            "pacote": pacote,
            "quantidade": item["qtd"],
            "hotel": hotel,
            "subtotal": subtotal
        })
>>>>>>> 1c8228b5a3fb9d6ec982ed510696cfa6d2fb7eb7

    return itens, total


# =====================================================
# VITRINE DE PACOTES
# =====================================================

def pacotes(request):
<<<<<<< HEAD
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
=======

    filtro = FiltroPacoteForm(
        request.GET or None
    )

    consulta = Pacote.objects.filter(
        ativo=True
    )

    somente_disponiveis = False

    if filtro.is_valid():

        dados = filtro.cleaned_data

        if dados["q"]:

            consulta = consulta.filter(
                Q(nome__icontains=dados["q"]) |
                Q(descricao__icontains=dados["q"])
            )

        if dados["preco_max"] is not None:

            consulta = consulta.filter(
                preco__lte=dados["preco_max"]
            )

        somente_disponiveis = dados["so_disponiveis"]

    elif filtro.is_bound:

        messages.error(
            request,
            resumo_erros(filtro)
        )

    hoteis = hoteis_por_pacote()

    lista = []

    for pacote in consulta:

        pacote.lista_hoteis = hoteis.get(
            pacote.pk,
            []
        )

        pacote.disponivel = any(
            hotel.livres > 0
            for hotel in pacote.lista_hoteis
        )

        if somente_disponiveis and not pacote.disponivel:
            continue

        lista.append(pacote)

    itens, total = obter_carrinho(request)

    return render(
        request,
        "core/pacotes.html",
        {
            "pacotes": lista,
            "itens": itens,
            "total": total,
            "filtro": filtro
        }
    )


# =====================================================
# ADICIONAR PACOTE AO CARRINHO
# =====================================================

@login_required
@require_POST
def adicionar_carrinho(request, pk):

    pacote = get_object_or_404(
        Pacote,
        pk=pk,
        ativo=True
    )

    form = AdicionarCarrinhoForm(
        request.POST,
        pacote=pacote
    )

    if not form.is_valid():

        messages.error(
            request,
            resumo_erros(form)
        )

        return redirect("pacotes")

    carrinho = request.session.get(
        "carrinho",
        {}
    )

    quantidade_anterior = item_carrinho(
        carrinho.get(str(pacote.pk), 0)
    )["qtd"]

    quantidade = (
        quantidade_anterior +
        form.cleaned_data["quantidade"]
    )

    if quantidade > MAX_VIAJANTES:

        messages.error(
            request,
            f"O limite é de {MAX_VIAJANTES} viajantes por pacote."
        )

        return redirect("pacotes")

    hoteis = hoteis_por_pacote().get(
        pacote.pk,
        []
    )

    if not hoteis:

        messages.error(
            request,
            "Este pacote ainda não possui hotéis cadastrados."
        )

        return redirect("pacotes")

    escolhido = form.cleaned_data["hotel"]

    if escolhido is None:

        hotel = max(
            hoteis,
            key=lambda h: h.livres
        )

    else:

        hotel = next(
            (h for h in hoteis if h.pk == escolhido.pk),
            None
        )

    if hotel is None:

        messages.error(
            request,
            "Hotel inválido para este pacote."
        )

        return redirect("pacotes")

    if hotel.livres < quantidade:

        messages.error(
            request,
            f"{hotel.nome} possui apenas {hotel.livres} vaga(s) disponíveis."
        )

        return redirect("pacotes")

    carrinho[str(pacote.pk)] = {
        "qtd": quantidade,
        "hotel": hotel.pk
    }

    request.session["carrinho"] = carrinho

    request.session.modified = True

    messages.success(
        request,
        "Pacote adicionado ao carrinho!"
    )

>>>>>>> 1c8228b5a3fb9d6ec982ed510696cfa6d2fb7eb7
    return redirect("pacotes")


# =====================================================
# REMOVER ITEM DO CARRINHO
# =====================================================

@require_POST
def remover_carrinho(request, pk):

    carrinho = request.session.get(
        "carrinho",
        {}
    )

    carrinho.pop(str(pk), None)

    request.session["carrinho"] = carrinho
<<<<<<< HEAD
    messages.success(request, "Item removido do carrinho.")
=======

    request.session.modified = True

    messages.success(
        request,
        "Item removido do carrinho."
    )

>>>>>>> 1c8228b5a3fb9d6ec982ed510696cfa6d2fb7eb7
    return redirect("pacotes")


# =====================================================
# FINALIZAR RESERVA
# =====================================================

@login_required
@require_POST
def finalizar_compra(request):
<<<<<<< HEAD
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

=======

    itens, total = obter_carrinho(request)

    if not itens:

        messages.warning(
            request,
            "Adicione pelo menos um pacote ao carrinho."
        )

        return redirect("pacotes")

    confirmadas = Compra.objects.filter(
        usuario=request.user,
        status=Compra.CONFIRMADA
    ).count()

    desconto = calcular_nivel(
        confirmadas
    )["desconto"]

    try:

        with transaction.atomic():

            for item in itens:

                criar_reserva(
                    usuario=request.user,
                    pacote=item["pacote"],
                    hotel=item["hotel"],
                    quantidade=item["quantidade"]
                )

    except (ValidationError, ValueError) as erro:

        messages.error(
            request,
            f"Não foi possível finalizar a reserva: {erro}"
        )

        return redirect("pacotes")

    request.session["carrinho"] = {}

    request.session.modified = True

    messages.success(
        request,
        f"Reserva confirmada! Desconto calculado: {desconto}%."
    )

    return redirect("perfil")


# =====================================================
# PERFIL DO CLIENTE
# =====================================================

@login_required
def perfil(request):

    reservas = request.user.compras.all()

    confirmadas = reservas.filter(
        status=Compra.CONFIRMADA
    )

    quantidade = confirmadas.count()

    total = confirmadas.aggregate(
        total=Sum("valor_final")
    )["total"] or Decimal("0.00")

    nivel = calcular_nivel(
        quantidade
    )

    return render(
        request,
        "core/perfil.html",
        {
            "compras": reservas,
            "qtd": quantidade,
            "total_gasto": total,
            "n": nivel
        }
    )


# =====================================================
# CANCELAR RESERVA
# =====================================================
>>>>>>> 1c8228b5a3fb9d6ec982ed510696cfa6d2fb7eb7

@login_required
@require_POST
def cancelar_reserva(request, pk):
<<<<<<< HEAD
    # filtrar por usuario impede cancelar a reserva de outra pessoa (retorna 404)
    reserva = get_object_or_404(Compra, pk=pk, usuario=request.user)

    try:
        reserva.cancelar()
        messages.success(request, f"Reserva de {reserva.destino} cancelada. As vagas foram liberadas.")
    except ValueError as erro:
        messages.warning(request, str(erro))
=======

    reserva = get_object_or_404(
        Compra,
        pk=pk,
        usuario=request.user
    )

    try:

        reserva.cancelar()

        messages.success(
            request,
            f"Reserva de {reserva.destino} cancelada. "
            "As vagas foram liberadas."
        )

    except ValueError as erro:

        messages.warning(
            request,
            str(erro)
        )
>>>>>>> 1c8228b5a3fb9d6ec982ed510696cfa6d2fb7eb7

    return redirect("perfil")


<<<<<<< HEAD
# ---------- gestão (administrador) ----------

@staff_required
def gestao_pacotes(request):
    busca = request.GET.get("q", "").strip()
    lista = Pacote.objects.all()

    if busca:
        lista = lista.filter(Q(nome__icontains=busca) | Q(descricao__icontains=busca))

    return render(request, "gestao_pacotes.html", {"pacotes": lista, "busca": busca})
=======
# =====================================================
# GESTÃO DE PACOTES
# =====================================================

@staff_required
def gestao_pacotes(request):

    busca = request.GET.get(
        "q",
        ""
    ).strip()

    lista = Pacote.objects.all()

    if busca:

        lista = lista.filter(
            Q(nome__icontains=busca) |
            Q(descricao__icontains=busca)
        )

    return render(
        request,
        "gestao/pacote_lista.html",
        {
            "pacotes": lista,
            "busca": busca
        }
    )
>>>>>>> 1c8228b5a3fb9d6ec982ed510696cfa6d2fb7eb7


@staff_required
def gestao_pacote_form(request, pk=None):
<<<<<<< HEAD
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
=======

    pacote = (
        get_object_or_404(Pacote, pk=pk)
        if pk else None
    )

    form = PacoteForm(
        request.POST or None,
        request.FILES or None,
        instance=pacote
    )

    if request.method == "POST" and form.is_valid():

        salvo = form.save()

        if pacote is None:

            messages.success(
                request,
                "Pacote criado! Agora cadastre os hotéis e as vagas."
            )

            return redirect(
                "gestao_pacote_editar",
                pk=salvo.pk
            )

        messages.success(
            request,
            "Pacote atualizado com sucesso."
        )

        return redirect("gestao_pacotes")

    return render(
        request,
        "gestao/pacote_form.html",
        {
            "form": form,
            "pacote": pacote,
            "titulo": "Editar pacote" if pacote else "Novo pacote"
        }
    )
>>>>>>> 1c8228b5a3fb9d6ec982ed510696cfa6d2fb7eb7


@staff_required
def gestao_pacote_excluir(request, pk):
<<<<<<< HEAD
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
=======

    pacote = get_object_or_404(
        Pacote,
        pk=pk
    )

    ativas = Compra.objects.filter(
        pacote=pacote,
        status=Compra.CONFIRMADA
    ).count()

    if ativas:

        messages.error(
            request,
            f"Existem {ativas} reserva(s) confirmada(s). "
            "Desative o pacote em vez de excluí-lo."
        )

        return redirect("gestao_pacotes")

    if request.method == "POST":

        pacote.delete()

        messages.success(
            request,
            "Pacote excluído com sucesso."
        )

        return redirect("gestao_pacotes")

    return render(
        request,
        "gestao/confirmar_exclusao.html",
        {
            "objeto": pacote,
            "voltar": "gestao_pacotes",
            "aviso": "Os hotéis deste pacote também serão excluídos."
        }
    )


# =====================================================
# GESTÃO DE HOTÉIS
# =====================================================

@staff_required
def gestao_hotel_form(request, pacote_pk=None, pk=None):

    if pk:

        hotel = get_object_or_404(
            Hotel,
            pk=pk
        )

        pacote = hotel.pacote

    else:

        pacote = get_object_or_404(
            Pacote,
            pk=pacote_pk
        )

        hotel = Hotel(
            pacote=pacote
        )

    form = HotelForm(
        request.POST or None,
        instance=hotel
    )

    if request.method == "POST" and form.is_valid():

        form.save()

        messages.success(
            request,
            "Hotel salvo com sucesso."
        )

        return redirect(
            "gestao_pacote_editar",
            pk=pacote.pk
        )

    return render(
        request,
        "gestao/form.html",
        {
            "form": form,
            "voltar": "gestao_pacote_editar",
            "voltar_pk": pacote.pk,
            "titulo": f"{'Editar' if pk else 'Novo'} hotel — {pacote.nome}"
        }
    )
>>>>>>> 1c8228b5a3fb9d6ec982ed510696cfa6d2fb7eb7


@staff_required
def gestao_hotel_excluir(request, pk):
<<<<<<< HEAD
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
=======

    hotel = get_object_or_404(
        Hotel,
        pk=pk
    )

    if hotel.ocupadas() > 0:

        messages.error(
            request,
            f"{hotel.nome} possui {hotel.ocupadas()} vaga(s) reservadas. "
            "Cancele as reservas antes de excluir."
        )

        return redirect(
            "gestao_pacote_editar",
            pk=hotel.pacote_id
        )

    if request.method == "POST":

        pacote_id = hotel.pacote_id

        hotel.delete()

        messages.success(
            request,
            "Hotel excluído com sucesso."
        )

        return redirect(
            "gestao_pacote_editar",
            pk=pacote_id
        )

    return render(
        request,
        "gestao/confirmar_exclusao.html",
        {
            "objeto": hotel,
            "voltar": "gestao_pacote_editar",
            "voltar_pk": hotel.pacote_id
        }
    )


# =====================================================
# GESTÃO DE RESERVAS
# =====================================================

@staff_required
def gestao_reservas(request):

    lista = Compra.objects.select_related(
        "usuario",
        "pacote",
        "hotel"
    )

    status = request.GET.get(
        "status",
        ""
    )

    busca = request.GET.get(
        "q",
        ""
    ).strip()

    if status in (
        Compra.CONFIRMADA,
        Compra.CANCELADA
    ):

        lista = lista.filter(
            status=status
        )

    if busca:

        lista = lista.filter(
            Q(usuario__email__icontains=busca) |
            Q(destino__icontains=busca)
        )

    return render(
        request,
        "gestao/reservas.html",
        {
            "reservas": lista,
            "status": status,
            "busca": busca
        }
    )
>>>>>>> 1c8228b5a3fb9d6ec982ed510696cfa6d2fb7eb7
