
from django.db import transaction
from django.db.models import Sum

from .models import Compra, Hotel
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

    if desconto is None:
        desconto = desconto_do_usuario(usuario)

    with transaction.atomic():

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
            .values("hotel")
            .annotate(total=Sum("quantidade"))
            .values_list("hotel", "total")
        )

        livres = {
            h.pk: h.vagas - (ocupadas.get(h.pk) or 0)
            for h in hoteis
        }

        if hotel is None:
            escolhido = max(hoteis, key=lambda h: livres[h.pk])
        else:
            escolhido = next(
                (h for h in hoteis if h.pk == hotel.pk),
                None
            )

            if escolhido is None:
                raise ValueError("O hotel não pertence a este pacote.")

        if livres[escolhido.pk] < quantidade:
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

        return Compra.objects.create(
            usuario=usuario,
            pacote=pacote,
            destino=pacote.nome,
            hotel=escolhido,
            hotel_nome=escolhido.nome,
            quantidade=quantidade,
            valor_original=original,
            desconto_percentual=desconto,
            valor_final=valor_final,
        )
