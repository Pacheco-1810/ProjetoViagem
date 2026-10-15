from django.contrib import admin

from .models import Compra, Orcamento, Pacote


@admin.register(Pacote)
class PacoteAdmin(admin.ModelAdmin):
    list_display = ("nome", "preco", "ativo", "no_carrossel", "ordem")
    list_editable = ("preco", "ativo", "no_carrossel", "ordem")
    list_filter = ("ativo", "no_carrossel")
    search_fields = ("nome", "descricao")


@admin.register(Compra)
class CompraAdmin(admin.ModelAdmin):
    list_display = ("destino", "usuario", "quantidade", "valor_original",
                    "desconto_percentual", "valor_final", "data")
    list_filter = ("destino", "data")
    search_fields = ("usuario__email", "usuario__first_name", "destino")
    date_hierarchy = "data"
    readonly_fields = ("data",)


@admin.register(Orcamento)
class OrcamentoAdmin(admin.ModelAdmin):
    list_display = ("nome", "email", "destino", "data_prevista", "viajantes",
                    "criado_em", "respondido")
    list_editable = ("respondido",)
    list_filter = ("respondido", "criado_em")
    search_fields = ("nome", "email", "destino", "mensagem")
    readonly_fields = ("criado_em",)
