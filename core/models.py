from django.conf import settings
from django.db import models


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


class Compra(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                related_name="compras", verbose_name="Cliente")
    pacote = models.ForeignKey(Pacote, on_delete=models.SET_NULL, null=True, blank=True,
                               verbose_name="Pacote")
    destino = models.CharField("Destino", max_length=100)
    quantidade = models.PositiveIntegerField("Viajantes", default=1)
    valor_original = models.DecimalField("Valor original (R$)", max_digits=12, decimal_places=2)
    desconto_percentual = models.PositiveIntegerField("Desconto (%)", default=0)
    valor_final = models.DecimalField("Valor final (R$)", max_digits=12, decimal_places=2)
    data = models.DateTimeField("Data da compra", auto_now_add=True)

    class Meta:
        ordering = ["data"]
        verbose_name = "Compra"
        verbose_name_plural = "Compras"

    def __str__(self):
        return f"{self.destino} - {self.usuario}"


class Orcamento(models.Model):
    nome = models.CharField(max_length=120)
    email = models.EmailField("E-mail")
    destino = models.CharField("Destino desejado", max_length=120)
    data_prevista = models.DateField("Data prevista", null=True, blank=True)
    viajantes = models.PositiveIntegerField("Nº de viajantes", default=1)
    mensagem = models.TextField("Descrição da viagem")
    criado_em = models.DateTimeField("Recebido em", auto_now_add=True)
    respondido = models.BooleanField("Respondido", default=False)

    class Meta:
        ordering = ["-criado_em"]
        verbose_name = "Pedido de orçamento"
        verbose_name_plural = "Pedidos de orçamento"

    def __str__(self):
        return f"{self.nome} - {self.destino}"
