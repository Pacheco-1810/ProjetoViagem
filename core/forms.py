from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm

from .models import Orcamento

User = get_user_model()


class LoginForm(AuthenticationForm):
    username = forms.EmailField(label="E-mail", widget=forms.EmailInput(
        attrs={"placeholder": "Digite seu e-mail", "autofocus": True}))
    password = forms.CharField(label="Senha", widget=forms.PasswordInput(
        attrs={"placeholder": "Digite sua senha"}))

    def clean_username(self):
        return self.cleaned_data["username"].lower()


class CadastroForm(forms.Form):
    nome = forms.CharField(label="Nome", max_length=150,
                           widget=forms.TextInput(attrs={"placeholder": "Digite seu nome"}))
    email = forms.EmailField(label="E-mail",
                             widget=forms.EmailInput(attrs={"placeholder": "Digite seu e-mail"}))
    senha = forms.CharField(label="Senha", min_length=6,
                            widget=forms.PasswordInput(attrs={"placeholder": "Digite sua senha"}))

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        if User.objects.filter(username=email).exists():
            raise forms.ValidationError("Já existe uma conta com este e-mail.")
        return email

    def save(self):
        d = self.cleaned_data
        return User.objects.create_user(username=d["email"], email=d["email"],
                                        password=d["senha"], first_name=d["nome"])


class OrcamentoForm(forms.ModelForm):
    class Meta:
        model = Orcamento
        fields = ["nome", "email", "destino", "data_prevista", "viajantes", "mensagem"]
        widgets = {
            "nome": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "destino": forms.TextInput(attrs={"class": "form-control",
                                              "placeholder": "Ex: Paris, Gramado, Cancún..."}),
            "data_prevista": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "viajantes": forms.NumberInput(attrs={"class": "form-control", "min": 1}),
            "mensagem": forms.Textarea(attrs={"class": "form-control", "rows": 5, "placeholder":
                "Informe detalhes, preferências, hotéis, passeios ou qualquer informação importante."}),
        }
