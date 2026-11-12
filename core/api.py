from drf_spectacular.utils import extend_schema
from rest_framework import filters, mixins, permissions, serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Compra, Hotel, Pacote
from .services import MAX_VIAJANTES, SemVaga, criar_reserva


class HotelSerializer(serializers.ModelSerializer):
    vagas_livres = serializers.IntegerField(source="disponiveis", read_only=True)

    class Meta:
        model = Hotel
        fields = ["id", "nome", "estrelas", "vagas", "acrescimo", "vagas_livres"]


class PacoteSerializer(serializers.ModelSerializer):
    hoteis = HotelSerializer(many=True, read_only=True)

    class Meta:
        model = Pacote
        fields = ["id", "nome", "descricao", "preco", "imagem", "ativo", "hoteis"]
        extra_kwargs = {"imagem": {"required": False}}

    def validate_nome(self, valor):
        valor = valor.strip()
        repetido = Pacote.objects.filter(nome__iexact=valor)
        if self.instance:
            repetido = repetido.exclude(pk=self.instance.pk)
        if repetido.exists():
            raise serializers.ValidationError("Já existe um pacote com este destino.")
        return valor

    def validate_preco(self, valor):
        if valor <= 0:
            raise serializers.ValidationError("O preço deve ser maior que zero.")
        return valor


class ReservaSerializer(serializers.ModelSerializer):
    pacote = serializers.PrimaryKeyRelatedField(queryset=Pacote.objects.filter(ativo=True))
    hotel = serializers.PrimaryKeyRelatedField(
        queryset=Hotel.objects.all(),
        required=False,
        allow_null=True,
        help_text="Opcional. Se não for informado, é usado o hotel com mais vagas.",
    )

    class Meta:
        model = Compra
        fields = [
            "id", "pacote", "hotel", "hotel_nome", "destino", "quantidade",
            "valor_original", "desconto_percentual", "valor_final", "status", "data",
        ]
        read_only_fields = [
            "id", "hotel_nome", "destino", "valor_original",
            "desconto_percentual", "valor_final", "status", "data",
        ]
        extra_kwargs = {"quantidade": {"min_value": 1, "max_value": MAX_VIAJANTES}}

    def validate(self, dados):
        hotel = dados.get("hotel")
        if hotel and hotel.pacote_id != dados["pacote"].pk:
            raise serializers.ValidationError({"hotel": "Este hotel não pertence ao pacote escolhido."})
        return dados

    def create(self, dados):
        try:
            return criar_reserva(
                usuario=self.context["request"].user,
                pacote=dados["pacote"],
                quantidade=dados["quantidade"],
                hotel=dados.get("hotel"),
            )
        except SemVaga as erro:
            raise serializers.ValidationError({"quantidade": [str(erro)]})
        except ValueError as erro:
            raise serializers.ValidationError({"hotel": [str(erro)]})


class IsStaffOrReadOnly(permissions.BasePermission):
    """Qualquer pessoa consulta; só administrador cadastra, edita ou exclui."""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated and request.user.is_staff)


class PacoteViewSet(viewsets.ModelViewSet):
    serializer_class = PacoteSerializer
    permission_classes = [IsStaffOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ["nome", "descricao"]

    def get_queryset(self):
        pacotes = Pacote.objects.prefetch_related("hoteis")
        # só o administrador vê os pacotes inativos
        if self.request.user.is_authenticated and self.request.user.is_staff:
            return pacotes
        return pacotes.filter(ativo=True)

    def perform_destroy(self, pacote):
        if Compra.objects.filter(pacote=pacote, status=Compra.CONFIRMADA).exists():
            raise serializers.ValidationError("Existem reservas confirmadas. Desative o pacote em vez de excluí-lo.")
        pacote.delete()


class ReservaViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = ReservaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):  # geração do Swagger, sem usuário
            return Compra.objects.none()

        reservas = Compra.objects.select_related("pacote", "hotel", "usuario")
        if self.request.user.is_staff:
            return reservas
        return reservas.filter(usuario=self.request.user)

    @extend_schema(summary="Cancelar reserva", request=None, responses={200: ReservaSerializer})
    @action(detail=True, methods=["post"])
    def cancelar(self, request, pk=None):
        reserva = self.get_object()
        try:
            reserva.cancelar()
        except ValueError as erro:
            return Response({"detail": str(erro)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(self.get_serializer(reserva).data)
