<<<<<<< HEAD
from decimal import Decimal
=======
>>>>>>> 1c8228b5a3fb9d6ec982ed510696cfa6d2fb7eb7

from django.db import transaction
from django.db.models import Sum

from .models import Compra, Hotel
<<<<<<< HEAD

MAX_VIAJANTES = 20

# (viagens mínimas, nome do nível, desconto em %)
NIVEIS = [
    (0, "Bronze", 5),
    (3, "Prata", 10),
    (6, "Ouro", 15),
    (10, "Diamante", 20),
]


class SemVaga(ValueError):
    pass


def calcular_nivel(viagens):
    atual = max(i for i, nivel in enumerate(NIVEIS) if viagens >= nivel[0])
    minimo, nome, desconto = NIVEIS[atual]

    if atual == len(NIVEIS) - 1:
        return {
            "nivel": nome,
            "desconto": desconto,
            "proximo": "Máximo",
            "progresso": 100,
            "texto": f"Parabéns! Você chegou ao nível máximo e tem {desconto}% de desconto.",
        }

    proximo_minimo, proximo_nome, _ = NIVEIS[atual + 1]
    return {
        "nivel": nome,
        "desconto": desconto,
        "proximo": proximo_nome,
        "progresso": round((viagens - minimo) / (proximo_minimo - minimo) * 100),
        "texto": f"Faltam {proximo_minimo - viagens} viagem(ns) para chegar ao nível {proximo_nome}.",
    }


def calcular_desconto(viagens):
    return calcular_nivel(viagens)["desconto"]


def desconto_do_usuario(usuario):
    return calcular_desconto(usuario.compras.filter(status=Compra.CONFIRMADA).count())


def criar_reserva(usuario, pacote, quantidade, hotel=None, desconto=None):
    if quantidade < 1 or quantidade > MAX_VIAJANTES:
        raise ValueError(f"A quantidade deve ser entre 1 e {MAX_VIAJANTES} viajantes.")
=======
from .niveis import calcular_desconto


MAX_VIAJANTES = 20


class SemVaga(Exception):
    """Erro quando não existem vagas suficientes para a reserva."""
    pass


def desconto_do_usuario(usuario):
    confirmadas = usuario.compras.filter(
        status=Compra.CONFIRMADA
    ).count()

    return calcular_desconto(confirmadas)


def criar_reserva(usuario, pacote, quantidade, hotel=None, desconto=None):

    if quantidade < 1 or quantidade > MAX_VIAJANTES:
        raise ValueError(
            f"A quantidade deve ser entre 1 e {MAX_VIAJANTES} viajantes."
        )
>>>>>>> 1c8228b5a3fb9d6ec982ed510696cfa6d2fb7eb7

    if desconto is None:
        desconto = desconto_do_usuario(usuario)

    with transaction.atomic():
<<<<<<< HEAD
        # select_for_update trava os hotéis para duas reservas não usarem a mesma vaga
        hoteis = list(Hotel.objects.select_for_update().filter(pacote=pacote).order_by("pk"))
        if not hoteis:
            raise SemVaga(f"O pacote {pacote.nome} ainda não possui hotéis cadastrados.")

        ocupadas = dict(
            Compra.objects.filter(hotel__in=hoteis, status=Compra.CONFIRMADA)
=======

        hoteis = list(
            Hotel.objects.select_for_update()
            .filter(pacote=pacote)
            .order_by("pk")
        )

        if not hoteis:
            raise SemVaga(
                f"O pacote {pacote.nome} ainda não possui hotéis cadastrados."
            )

        ocupadas = dict(
            Compra.objects.filter(
                hotel__in=hoteis,
                status=Compra.CONFIRMADA
            )
>>>>>>> 1c8228b5a3fb9d6ec982ed510696cfa6d2fb7eb7
            .values("hotel")
            .annotate(total=Sum("quantidade"))
            .values_list("hotel", "total")
        )
<<<<<<< HEAD
        livres = {h.pk: h.vagas - ocupadas.get(h.pk, 0) for h in hoteis}
=======

        livres = {
            h.pk: h.vagas - (ocupadas.get(h.pk) or 0)
            for h in hoteis
        }
>>>>>>> 1c8228b5a3fb9d6ec982ed510696cfa6d2fb7eb7

        if hotel is None:
            escolhido = max(hoteis, key=lambda h: livres[h.pk])
        else:
<<<<<<< HEAD
            escolhido = next((h for h in hoteis if h.pk == hotel.pk), None)
=======
            escolhido = next(
                (h for h in hoteis if h.pk == hotel.pk),
                None
            )

>>>>>>> 1c8228b5a3fb9d6ec982ed510696cfa6d2fb7eb7
            if escolhido is None:
                raise ValueError("O hotel não pertence a este pacote.")

        if livres[escolhido.pk] < quantidade:
<<<<<<< HEAD
            raise SemVaga(f"{escolhido.nome} possui apenas {max(livres[escolhido.pk], 0)} vaga(s).")

        valor_original = (pacote.preco + escolhido.acrescimo) * quantidade
        valor_final = (valor_original * (100 - desconto) / 100).quantize(Decimal("0.01"))
=======
            restantes = max(livres[escolhido.pk], 0)

            raise SemVaga(
                f"{escolhido.nome} possui apenas {restantes} vaga(s)."
            )

        original = (
            pacote.preco + escolhido.acrescimo
        ) * quantidade

        valor_final = original - (
            original * desconto / 100
        )
>>>>>>> 1c8228b5a3fb9d6ec982ed510696cfa6d2fb7eb7

        return Compra.objects.create(
            usuario=usuario,
            pacote=pacote,
            destino=pacote.nome,
            hotel=escolhido,
            hotel_nome=escolhido.nome,
            quantidade=quantidade,
<<<<<<< HEAD
            valor_original=valor_original,
=======
            valor_original=original,
>>>>>>> 1c8228b5a3fb9d6ec982ed510696cfa6d2fb7eb7
            desconto_percentual=desconto,
            valor_final=valor_final,
        )
