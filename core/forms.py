from decimal import Decimal

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.password_validation import validate_password
from django.utils import timezone

from .models import Hotel, Orcamento, Pacote
from .services import MAX_VIAJANTES

User = get_user_model()


class BootstrapMixin:
    """Coloca as classes do Bootstrap em todos os campos."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for campo in self.fields.values():
            if isinstance(campo.widget, forms.CheckboxInput):
                campo.widget.attrs["class"] = "form-check-input"
            elif isinstance(campo.widget, forms.Select):
                campo.widget.attrs["class"] = "form-select"
            else:
                campo.widget.attrs["class"] = "form-control"


class LoginForm(BootstrapMixin, AuthenticationForm):
    username = forms.CharField(label="E-mail", widget=forms.TextInput(attrs={"autofocus": True}))
    password = forms.CharField(label="Senha", widget=forms.PasswordInput)

    def clean_username(self):
        usuario = self.cleaned_data["username"].strip()
        return usuario.lower() if "@" in usuario else usuario


class CadastroForm(BootstrapMixin, forms.Form):
    nome = forms.CharField(label="Nome completo", max_length=150)
    email = forms.EmailField(label="E-mail")
    senha = forms.CharField(label="Senha", min_length=8, widget=forms.PasswordInput)

    def clean_nome(self):
        nome = self.cleaned_data["nome"].strip()
        if not nome:
            raise forms.ValidationError("Informe seu nome.")
        return nome

    def clean_email(self):
        email = self.cleaned_data["email"].lower().strip()
        if User.objects.filter(username__iexact=email).exists():
            raise forms.ValidationError("Já existe uma conta com este e-mail.")
        return email

    def clean_senha(self):
        senha = self.cleaned_data["senha"]
        validate_password(senha)
        return senha

    def save(self):
        dados = self.cleaned_data
        return User.objects.create_user(
            username=dados["email"],
            email=dados["email"],
            password=dados["senha"],
            first_name=dados["nome"],
        )


class OrcamentoForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = Orcamento
        fields = ["nome", "email", "destino", "data_prevista", "viajantes", "mensagem"]
        widgets = {
            "data_prevista": forms.DateInput(attrs={"type": "date"}),
            "mensagem": forms.Textarea(attrs={"rows": 5}),
        }

    def clean_data_prevista(self):
        data = self.cleaned_data["data_prevista"]
        if data and data < timezone.localdate():
            raise forms.ValidationError("A data prevista não pode estar no passado.")
        return data


class PacoteForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = Pacote
        fields = ["nome", "descricao", "preco", "imagem", "ativo", "no_carrossel", "legenda_carrossel", "ordem"]
        widgets = {"preco": forms.NumberInput(attrs={"min": "0.01", "step": "0.01"})}

    def clean_nome(self):
        nome = self.cleaned_data["nome"].strip()
        if Pacote.objects.filter(nome__iexact=nome).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Já existe um pacote com este destino.")
        return nome

    def clean_preco(self):
        preco = self.cleaned_data["preco"]
        if preco <= Decimal("0"):
            raise forms.ValidationError("O preço deve ser maior que zero.")
        return preco

    def clean(self):
        dados = super().clean()
        if dados.get("no_carrossel") and not dados.get("legenda_carrossel"):
            self.add_error("legenda_carrossel", "Informe a legenda para exibir o pacote no carrossel.")
        return dados


class HotelForm(BootstrapMixin, forms.ModelForm):
    # as regras (nome repetido, vagas menores que as reservas) estão em Hotel.clean()
    class Meta:
        model = Hotel
        fields = ["nome", "estrelas", "vagas", "acrescimo"]


class AdicionarCarrinhoForm(BootstrapMixin, forms.Form):
    quantidade = forms.IntegerField(label="Quantidade de viajantes", min_value=1, max_value=MAX_VIAJANTES)
    hotel = forms.ModelChoiceField(
        label="Hotel", queryset=Hotel.objects.none(), required=False, empty_label="Escolher automaticamente"
    )

    def __init__(self, *args, pacote, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["hotel"].queryset = pacote.hoteis.all()


class FiltroPacoteForm(BootstrapMixin, forms.Form):
    q = forms.CharField(label="Destino", required=False, max_length=100)
    preco_max = forms.DecimalField(label="Preço máximo (R$)", required=False, min_value=0, max_digits=10, decimal_places=2)
    so_disponiveis = forms.BooleanField(label="Somente pacotes com vagas", required=False)
