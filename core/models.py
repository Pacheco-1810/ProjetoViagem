from decimal import Decimal

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Sum


class Pacote(models.Model):
    nome = models.CharField("Destino", max_length=100)
    descricao = models.CharField("Descrição", max_length=255)
    preco = models.DecimalField("Preço por viajante (R$)", max_digits=10, decimal_places=2)
    imagem = models.ImageField("Imagem", upload_to="pacotes/")
    ativo = models.BooleanField("Disponível para venda", default=True)
    no_carrossel = models.BooleanField("Exibir no carrossel da página inicial", default=False)
    legenda_carrossel = models.CharField("Legenda do carrossel", max_length=150, blank=True)
    ordem = models.PositiveIntegerField("Ordem de exibição", default=0)

    class Meta:
        ordering = ["ordem", "nome"]
        verbose_name = "Pacote"
        verbose_name_plural = "Pacotes"

    def __str__(self):
        return self.nome

    def tem_vagas(self):
        return any(hotel.disponiveis() > 0 for hotel in self.hoteis.all())


class Hotel(models.Model):
    pacote = models.ForeignKey(Pacote, on_delete=models.CASCADE, related_name="hoteis", verbose_name="Pacote")
    nome = models.CharField("Nome", max_length=100)
    estrelas = models.PositiveIntegerField(
        "Estrelas", default=3, validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    vagas = models.PositiveIntegerField("Vagas (viajantes)", validators=[MinValueValidator(1)])
    acrescimo = models.DecimalField(
        "Acréscimo por viajante (R$)",
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(Decimal("0.00"))],
    )

    class Meta:
        ordering = ["nome"]
        verbose_name = "Hotel"
        verbose_name_plural = "Hotéis"

    def __str__(self):
        return f"{self.nome} ({self.pacote.nome})"

    def clean(self):
        # vale para o admin e para as telas de gestão
        if self.pacote_id and self.nome:
            repetido = Hotel.objects.filter(pacote_id=self.pacote_id, nome__iexact=self.nome.strip())
            if repetido.exclude(pk=self.pk).exists():
                raise ValidationError({"nome": "Este pacote já possui um hotel com esse nome."})

        if self.pk and self.vagas is not None and self.vagas < self.ocupadas():
            raise ValidationError(
                {"vagas": f"Já existem {self.ocupadas()} vaga(s) reservadas. A capacidade não pode ser menor."}
            )

    def ocupadas(self):
        total = self.compras.filter(status=Compra.CONFIRMADA).aggregate(total=Sum("quantidade"))["total"]
        return total or 0

    def disponiveis(self):
        return max(self.vagas - self.ocupadas(), 0)


class Compra(models.Model):
    CONFIRMADA = "confirmada"
    CANCELADA = "cancelada"
    STATUS = [(CONFIRMADA, "Confirmada"), (CANCELADA, "Cancelada")]

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="compras", verbose_name="Cliente"
    )
    pacote = models.ForeignKey(Pacote, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Pacote")
    hotel = models.ForeignKey(
        Hotel, on_delete=models.SET_NULL, null=True, blank=True, related_name="compras", verbose_name="Hotel"
    )
    hotel_nome = models.CharField("Hotel (na época)", max_length=100, blank=True)
    destino = models.CharField("Destino", max_length=100)
    quantidade = models.PositiveIntegerField("Viajantes", default=1, validators=[MinValueValidator(1)])
    valor_original = models.DecimalField("Valor original (R$)", max_digits=12, decimal_places=2)
    desconto_percentual = models.PositiveIntegerField(
        "Desconto (%)", default=0, validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    valor_final = models.DecimalField("Valor final (R$)", max_digits=12, decimal_places=2)
    status = models.CharField("Status", max_length=10, choices=STATUS, default=CONFIRMADA)
    data = models.DateTimeField("Data da compra", auto_now_add=True)

    class Meta:
        ordering = ["data"]
        verbose_name = "Compra"
        verbose_name_plural = "Compras"

    def __str__(self):
        return f"{self.destino} - {self.usuario}"

    def cancelar(self):
        if self.status != self.CONFIRMADA:
            raise ValueError("Esta reserva já está cancelada.")
        self.status = self.CANCELADA
        self.save(update_fields=["status"])


class Orcamento(models.Model):
    nome = models.CharField(max_length=120)
    email = models.EmailField("E-mail")
    destino = models.CharField("Destino desejado", max_length=120)
    data_prevista = models.DateField("Data prevista", null=True, blank=True)
    viajantes = models.PositiveIntegerField("Nº de viajantes", default=1, validators=[MinValueValidator(1)])
    mensagem = models.TextField("Descrição da viagem")
    criado_em = models.DateTimeField("Recebido em", auto_now_add=True)
    respondido = models.BooleanField("Respondido", default=False)

    class Meta:
        ordering = ["-criado_em"]
        verbose_name = "Pedido de orçamento"
        verbose_name_plural = "Pedidos de orçamento"

    def __str__(self):
        return f"{self.nome} - {self.destino}"
