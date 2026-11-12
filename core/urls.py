from django.contrib.auth import views as auth_views
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.routers import DefaultRouter

from . import views
from .api import PacoteViewSet, ReservaViewSet
from .forms import LoginForm

router = DefaultRouter()
router.register("pacotes", PacoteViewSet, basename="api-pacote")
router.register("reservas", ReservaViewSet, basename="api-reserva")

urlpatterns = [
    path("", views.index, name="index"),
    path("pacotes/", views.pacotes, name="pacotes"),
    path("sobre/", views.sobre, name="sobre"),
    path("contato/", views.contato, name="contato"),

    path("login/", auth_views.LoginView.as_view(authentication_form=LoginForm, template_name="login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("cadastro/", views.cadastro, name="cadastro"),

    path("carrinho/adicionar/<int:pk>/", views.adicionar_carrinho, name="adicionar_carrinho"),
    path("carrinho/remover/<int:pk>/", views.remover_carrinho, name="remover_carrinho"),
    path("carrinho/finalizar/", views.finalizar_compra, name="finalizar_compra"),

    path("perfil/", views.perfil, name="perfil"),
    path("reserva/<int:pk>/cancelar/", views.cancelar_reserva, name="cancelar_reserva"),

    path("gestao/", views.gestao_pacotes, name="gestao_pacotes"),
    path("gestao/pacotes/novo/", views.gestao_pacote_form, name="gestao_pacote_novo"),
    path("gestao/pacotes/<int:pk>/editar/", views.gestao_pacote_form, name="gestao_pacote_editar"),
    path("gestao/pacotes/<int:pk>/excluir/", views.gestao_pacote_excluir, name="gestao_pacote_excluir"),
    path("gestao/pacotes/<int:pacote_pk>/hoteis/novo/", views.gestao_hotel_form, name="gestao_hotel_novo"),
    path("gestao/hoteis/<int:pk>/editar/", views.gestao_hotel_form, name="gestao_hotel_editar"),
    path("gestao/hoteis/<int:pk>/excluir/", views.gestao_hotel_excluir, name="gestao_hotel_excluir"),
    path("gestao/reservas/", views.gestao_reservas, name="gestao_reservas"),

    path("api/schema/", SpectacularAPIView.as_view(), name="api-schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="api-schema"), name="api-docs"),
    path("api/", include(router.urls)),
]
