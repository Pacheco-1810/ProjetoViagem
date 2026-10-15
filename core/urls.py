from django.contrib.auth import views as auth_views
from django.urls import path

from . import views
from .forms import LoginForm

urlpatterns = [
    path("", views.index, name="index"),
    path("pacotes/", views.pacotes, name="pacotes"),
    path("sobre/", views.sobre, name="sobre"),
    path("contato/", views.contato, name="contato"),
    path("perfil/", views.perfil, name="perfil"),
    path("carrinho/adicionar/<int:pk>/", views.adicionar_carrinho, name="adicionar_carrinho"),
    path("carrinho/remover/<int:pk>/", views.remover_carrinho, name="remover_carrinho"),
    path("carrinho/finalizar/", views.finalizar_compra, name="finalizar_compra"),
    path("login/", auth_views.LoginView.as_view(authentication_form=LoginForm), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("cadastro/", views.cadastro, name="cadastro"),
]
