from django.contrib.auth import views as auth_views
from django.urls import path

from . import views
from .forms import LoginForm

urlpatterns = [
    # Páginas principais
    path("", views.index, name="index"),
    path("pacotes/", views.pacotes, name="pacotes"),
    path("sobre/", views.sobre, name="sobre"),
    path("contato/", views.contato, name="contato"),

    # Perfil do cliente
    path("perfil/", views.perfil, name="perfil"),
    path("reserva/<int:pk>/cancelar/", views.cancelar_reserva, name="cancelar_reserva"),

    # Carrinho de compras
    path("carrinho/adicionar/<int:pk>/", views.adicionar_carrinho, name="adicionar_carrinho"),
    path("carrinho/remover/<int:pk>/", views.remover_carrinho, name="remover_carrinho"),
    path("carrinho/finalizar/", views.finalizar_compra, name="finalizar_compra"),

    # Autenticação
    path("login/", auth_views.LoginView.as_view(authentication_form=LoginForm), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("cadastro/", views.cadastro, name="cadastro"),

    # Gestão (administrador)
    path("gestao/", views.gestao_pacotes, name="gestao"),
    path("gestao/pacotes/", views.gestao_pacotes, name="gestao_pacotes"),
    path("gestao/pacotes/novo/", views.gestao_pacote_form, name="gestao_pacote_novo"),
    path("gestao/pacotes/<int:pk>/editar/", views.gestao_pacote_form, name="gestao_pacote_editar"),
    path("gestao/pacotes/<int:pk>/excluir/", views.gestao_pacote_excluir, name="gestao_pacote_excluir"),

    # Gestão de hotéis
    path("gestao/pacotes/<int:pacote_pk>/hoteis/novo/", views.gestao_hotel_form, name="gestao_hotel_novo"),
    path("gestao/hoteis/<int:pk>/editar/", views.gestao_hotel_form, name="gestao_hotel_editar"),
    path("gestao/hoteis/<int:pk>/excluir/", views.gestao_hotel_excluir, name="gestao_hotel_excluir"),

    # Gestão de reservas
    path("gestao/reservas/", views.gestao_reservas, name="gestao_reservas"),
]

