
from drf_spectacular.utils import extend_schema

from rest_framework import (
    filters,
    mixins,
    permissions,
    status,
    viewsets,
)

from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Compra, Pacote
from .Serializers import PacoteSerializer, ReservaSerializer


# =====================================================
# PERMISSÕES
# =====================================================

class IsStaffOrReadOnly(permissions.BasePermission):
    """
    Qualquer pessoa pode consultar os pacotes.
    Somente administradores podem cadastrar,
    editar ou excluir.
    """

    def has_permission(self, request, view):

        if request.method in permissions.SAFE_METHODS:
            return True

        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.is_staff
        )


# =====================================================
# API DE PACOTES
# =====================================================

class PacoteViewSet(viewsets.ModelViewSet):

    serializer_class = PacoteSerializer

    permission_classes = [IsStaffOrReadOnly]

    filter_backends = [
        filters.SearchFilter,
    ]

    search_fields = [
        "nome",
        "descricao",
    ]

    def get_queryset(self):

        pacotes = Pacote.objects.prefetch_related(
            "hoteis"
        )

        # Administradores visualizam todos os pacotes.
        if (
            self.request.user and
            self.request.user.is_authenticated and
            self.request.user.is_staff
        ):
            return pacotes

        # Visitantes e clientes visualizam somente ativos.
        return pacotes.filter(
            ativo=True
        )


# =====================================================
# API DE RESERVAS
# =====================================================

class ReservaViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):

    serializer_class = ReservaSerializer

    permission_classes = [
        permissions.IsAuthenticated
    ]

    def get_queryset(self):

        # Evita problemas na geração do Swagger.
        if getattr(
            self,
            "swagger_fake_view",
            False
        ):
            return Compra.objects.none()

        reservas = Compra.objects.select_related(
            "pacote",
            "hotel",
            "usuario",
        )

        # Administrador pode consultar todas.
        if self.request.user.is_staff:
            return reservas

        # Cliente consulta somente suas reservas.
        return reservas.filter(
            usuario=self.request.user
        )

    # =========================================
    # CANCELAR RESERVA
    # =========================================

    @extend_schema(
        summary="Cancelar reserva",
        description=(
            "Cancela uma reserva confirmada. "
            "O cliente só pode cancelar suas próprias reservas. "
            "O administrador pode cancelar qualquer reserva."
        ),
        request=None,
        responses={
            200: ReservaSerializer,
            400: None,
            404: None,
        },
    )

    @action(
        detail=True,
        methods=["post"],
        url_path="cancelar",
    )
    def cancelar(self, request, pk=None):

        reserva = self.get_object()

        try:

            reserva.cancelar()

        except ValueError as erro:

            return Response(
                {
                    "detail": str(erro)
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            self.get_serializer(reserva).data,
            status=status.HTTP_200_OK,
        )
