
from rest_framework import serializers

from .models import Compra, Hotel, Pacote
from .services import MAX_VIAJANTES, SemVaga, criar_reserva


# =====================================================
# SERIALIZER DE HOTÉIS
# =====================================================

class HotelSerializer(serializers.ModelSerializer):

    vagas_livres = serializers.IntegerField(
        source="disponiveis",
        read_only=True
    )

    class Meta:
        model = Hotel

        fields = [
            "id",
            "nome",
            "estrelas",
            "vagas",
            "acrescimo",
            "vagas_livres",
        ]


# =====================================================
# SERIALIZER DE PACOTES
# =====================================================

class PacoteSerializer(serializers.ModelSerializer):

    hoteis = HotelSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = Pacote

        fields = [
            "id",
            "nome",
            "descricao",
            "preco",
            "imagem",
            "ativo",
            "hoteis",
        ]

        extra_kwargs = {
            "imagem": {
                "required": False
            }
        }

    def validate_nome(self, valor):

        valor = valor.strip()

        repetido = Pacote.objects.filter(
            nome__iexact=valor
        )

        if self.instance:
            repetido = repetido.exclude(
                pk=self.instance.pk
            )

        if repetido.exists():
            raise serializers.ValidationError(
                "Já existe um pacote com este destino."
            )

        return valor

    def validate_preco(self, valor):

        if valor <= 0:
            raise serializers.ValidationError(
                "O preço deve ser maior que zero."
            )

        return valor


# =====================================================
# SERIALIZER DE RESERVAS
# =====================================================

class ReservaSerializer(serializers.ModelSerializer):

    pacote = serializers.PrimaryKeyRelatedField(
        queryset=Pacote.objects.filter(ativo=True)
    )

    hotel = serializers.PrimaryKeyRelatedField(
        queryset=Hotel.objects.all(),
        required=False,
        allow_null=True,
        help_text=(
            "Opcional. Caso não seja informado, "
            "o sistema selecionará o hotel com mais vagas."
        )
    )

    class Meta:
        model = Compra

        fields = [
            "id",
            "pacote",
            "hotel",
            "hotel_nome",
            "destino",
            "quantidade",
            "valor_original",
            "desconto_percentual",
            "valor_final",
            "status",
            "data",
        ]

        read_only_fields = [
            "id",
            "hotel_nome",
            "destino",
            "valor_original",
            "desconto_percentual",
            "valor_final",
            "status",
            "data",
        ]

        extra_kwargs = {
            "quantidade": {
                "min_value": 1,
                "max_value": MAX_VIAJANTES,
            }
        }

    def validate(self, dados):

        pacote = dados["pacote"]
        hotel = dados.get("hotel")

        if hotel and hotel.pacote_id != pacote.pk:

            raise serializers.ValidationError({
                "hotel": (
                    "Este hotel não pertence ao pacote escolhido."
                )
            })

        return dados

    def create(self, dados):

        usuario = self.context["request"].user

        try:

            reserva = criar_reserva(
                usuario=usuario,
                pacote=dados["pacote"],
                quantidade=dados["quantidade"],
                hotel=dados.get("hotel"),
            )

            return reserva

        except SemVaga as erro:

            raise serializers.ValidationError({
                "quantidade": [str(erro)]
            })

        except ValueError as erro:

            raise serializers.ValidationError({
                "hotel": [str(erro)]
            })
