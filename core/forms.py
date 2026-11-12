<<<<<<< HEAD
=======

>>>>>>> 1c8228b5a3fb9d6ec982ed510696cfa6d2fb7eb7
from decimal import Decimal

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.password_validation import validate_password
from django.utils import timezone
<<<<<<< HEAD

from .models import Hotel, Orcamento, Pacote
from .services import MAX_VIAJANTES
=======

from .models import Hotel, Orcamento, Pacote
from .services import MAX_VIAJANTES

>>>>>>> 1c8228b5a3fb9d6ec982ed510696cfa6d2fb7eb7

User = get_user_model()


<<<<<<< HEAD
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
=======
# =====================================================
# LOGIN
# =====================================================

class LoginForm(AuthenticationForm):

    username = forms.EmailField(
        label="E-mail",
        widget=forms.EmailInput(attrs={
            "class": "form-control",
            "placeholder": "Digite seu e-mail",
            "autofocus": True,
        })
    )

    password = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Digite sua senha",
        })
    )

    def clean_username(self):
        return self.cleaned_data["username"].lower().strip()


# =====================================================
# CADASTRO DE CLIENTES
# =====================================================

class CadastroForm(forms.Form):

    nome = forms.CharField(
        label="Nome completo",
        max_length=150,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Digite seu nome",
        })
    )

    email = forms.EmailField(
        label="E-mail",
        widget=forms.EmailInput(attrs={
            "class": "form-control",
            "placeholder": "Digite seu e-mail",
        })
    )

    senha = forms.CharField(
        label="Senha",
        min_length=8,
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Digite sua senha",
        })
    )

    def clean_nome(self):
        nome = self.cleaned_data["nome"].strip()

        if not nome:
            raise forms.ValidationError(
                "Informe seu nome."
            )

>>>>>>> 1c8228b5a3fb9d6ec982ed510696cfa6d2fb7eb7
        return nome

    def clean_email(self):
        email = self.cleaned_data["email"].lower().strip()
<<<<<<< HEAD
        if User.objects.filter(username__iexact=email).exists():
            raise forms.ValidationError("Já existe uma conta com este e-mail.")
=======

        if User.objects.filter(username__iexact=email).exists():
            raise forms.ValidationError(
                "Já existe uma conta com este e-mail."
            )

>>>>>>> 1c8228b5a3fb9d6ec982ed510696cfa6d2fb7eb7
        return email

    def clean_senha(self):
        senha = self.cleaned_data["senha"]
        validate_password(senha)
        return senha
<<<<<<< HEAD

    def save(self):
        dados = self.cleaned_data
        return User.objects.create_user(
            username=dados["email"],
            email=dados["email"],
            password=dados["senha"],
            first_name=dados["nome"],
        )
=======
>>>>>>> 1c8228b5a3fb9d6ec982ed510696cfa6d2fb7eb7

    def save(self):
        dados = self.cleaned_data

        return User.objects.create_user(
            username=dados["email"],
            email=dados["email"],
            password=dados["senha"],
            first_name=dados["nome"],
        )


# =====================================================
# SOLICITAÇÃO DE ORÇAMENTO
# =====================================================

<<<<<<< HEAD
class OrcamentoForm(BootstrapMixin, forms.ModelForm):
=======
class OrcamentoForm(forms.ModelForm):

    viajantes = forms.IntegerField(
        label="Número de viajantes",
        min_value=1,
        initial=1,
    )

>>>>>>> 1c8228b5a3fb9d6ec982ed510696cfa6d2fb7eb7
    class Meta:
        model = Orcamento

        fields = [
            "nome",
            "email",
            "destino",
            "data_prevista",
            "viajantes",
            "mensagem",
        ]

        widgets = {
<<<<<<< HEAD
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
=======
            "nome": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Seu nome",
            }),

            "email": forms.EmailInput(attrs={
                "class": "form-control",
                "placeholder": "Seu e-mail",
            }),

            "destino": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Ex: Paris, Gramado, Cancún",
            }),

            "data_prevista": forms.DateInput(attrs={
                "class": "form-control",
                "type": "date",
            }),

            "viajantes": forms.NumberInput(attrs={
                "class": "form-control",
                "min": 1,
            }),

            "mensagem": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 5,
                "placeholder": "Conte mais sobre sua viagem...",
            }),
        }

    def clean_data_prevista(self):
        data = self.cleaned_data.get("data_prevista")

        if data and data < timezone.localdate():
            raise forms.ValidationError(
                "A data prevista não pode estar no passado."
            )

        return data


# =====================================================
# CONFIGURAÇÃO DE CLASSES BOOTSTRAP
# =====================================================

class BootstrapMixin:
    """Aplica classes Bootstrap aos campos dos formulários."""

    def aplicar_bootstrap(self):

        for campo in self.fields.values():

            widget = campo.widget

            if isinstance(widget, forms.CheckboxInput):
                classe = "form-check-input"

            elif isinstance(
                widget,
                (forms.Select, forms.SelectMultiple)
            ):
                classe = "form-select"

            else:
                classe = "form-control"

            classes_atuais = widget.attrs.get("class", "")

            if classe not in classes_atuais.split():
                widget.attrs["class"] = (
                    classes_atuais + " " + classe
                ).strip()


# =====================================================
# CADASTRO E EDIÇÃO DE PACOTES
# =====================================================

class PacoteForm(BootstrapMixin, forms.ModelForm):

    class Meta:
        model = Pacote

        fields = [
            "nome",
            "descricao",
            "preco",
            "imagem",
            "ativo",
            "no_carrossel",
            "legenda_carrossel",
            "ordem",
        ]

        widgets = {
            "nome": forms.TextInput(attrs={
                "placeholder": "Nome do destino",
            }),

            "descricao": forms.Textarea(attrs={
                "rows": 3,
            }),

            "preco": forms.NumberInput(attrs={
                "min": "0.01",
                "step": "0.01",
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.aplicar_bootstrap()

    def clean_nome(self):

        nome = self.cleaned_data["nome"].strip()

        repetido = Pacote.objects.filter(
            nome__iexact=nome
        ).exclude(
            pk=self.instance.pk
        )

        if repetido.exists():
            raise forms.ValidationError(
                "Já existe um pacote com este destino."
            )

>>>>>>> 1c8228b5a3fb9d6ec982ed510696cfa6d2fb7eb7
        return nome

    def clean_preco(self):
        preco = self.cleaned_data["preco"]
<<<<<<< HEAD
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
=======

        if preco <= Decimal("0.00"):
            raise forms.ValidationError(
                "O preço deve ser maior que zero."
            )

        return preco

    def clean(self):

        dados = super().clean()

        if dados.get("no_carrossel") and not dados.get(
            "legenda_carrossel"
        ):
            self.add_error(
                "legenda_carrossel",
                "Informe a legenda para exibir o pacote no carrossel."
            )

        return dados


# =====================================================
# CADASTRO E EDIÇÃO DE HOTÉIS
# =====================================================

class HotelForm(BootstrapMixin, forms.ModelForm):

    estrelas = forms.IntegerField(
        min_value=1,
        max_value=5,
        initial=3,
    )

    vagas = forms.IntegerField(
        min_value=1,
    )

    acrescimo = forms.DecimalField(
        min_value=0,
        max_digits=10,
        decimal_places=2,
        initial=Decimal("0.00"),
    )

    class Meta:
        model = Hotel

        fields = [
            "nome",
            "estrelas",
            "vagas",
            "acrescimo",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.aplicar_bootstrap()

    def clean_nome(self):

        nome = self.cleaned_data["nome"].strip()

        repetido = Hotel.objects.filter(
            pacote_id=self.instance.pacote_id,
            nome__iexact=nome,
        ).exclude(
            pk=self.instance.pk
        )

        if repetido.exists():
            raise forms.ValidationError(
                "Este pacote já possui um hotel com esse nome."
            )

        return nome

    def clean_vagas(self):

        vagas = self.cleaned_data["vagas"]

        if self.instance.pk:

            ocupadas = self.instance.ocupadas()

            if vagas < ocupadas:
                raise forms.ValidationError(
                    f"Já existem {ocupadas} vaga(s) reservadas. "
                    "Não é possível definir uma capacidade menor."
                )

        return vagas


# =====================================================
# ADICIONAR PACOTE AO CARRINHO
# =====================================================

class AdicionarCarrinhoForm(forms.Form):

    quantidade = forms.IntegerField(
        label="Quantidade de viajantes",
        min_value=1,
        max_value=MAX_VIAJANTES,
    )

    hotel = forms.ModelChoiceField(
        label="Hotel",
        queryset=Hotel.objects.none(),
        required=False,
        empty_label="Escolher automaticamente",
    )

    def __init__(self, *args, pacote, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields["hotel"].queryset = pacote.hoteis.all()

        self.fields["quantidade"].widget.attrs.update({
            "class": "form-control",
            "min": 1,
            "max": MAX_VIAJANTES,
        })

        self.fields["hotel"].widget.attrs.update({
            "class": "form-select",
        })


# =====================================================
# FILTRO DE PACOTES
# =====================================================

class FiltroPacoteForm(BootstrapMixin, forms.Form):

    q = forms.CharField(
        label="Destino",
        required=False,
        max_length=100,
        widget=forms.TextInput(attrs={
            "placeholder": "Buscar destino...",
        })
    )

    preco_max = forms.DecimalField(
        label="Preço máximo",
        required=False,
        min_value=0,
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            "placeholder": "Preço máximo (R$)",
            "step": "0.01",
        })
    )

    so_disponiveis = forms.BooleanField(
        label="Somente pacotes com vagas",
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.aplicar_bootstrap()
>>>>>>> 1c8228b5a3fb9d6ec982ed510696cfa6d2fb7eb7
