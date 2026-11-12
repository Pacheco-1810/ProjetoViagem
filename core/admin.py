from django.contrib import admin

from .models import Compra, Hotel, Orcamento, Pacote


class HotelInline(admin.TabularInline):
    model = Hotel
    extra = 1


@admin.register(Pacote)
class PacoteAdmin(admin.ModelAdmin):
    list_display = ("nome", "preco", "ativo", "no_carrossel", "ordem", "hoteis_cadastrados")
    list_editable = ("preco", "ativo", "no_carrossel", "ordem")
    list_filter = ("ativo", "no_carrossel")
    search_fields = ("nome", "descricao")
    inlines = [HotelInline]

    @admin.display(description="Hotéis")
    def hoteis_cadastrados(self, pacote):
        return pacote.hoteis.count()

    def has_delete_permission(self, request, obj=None):
        if obj and Compra.objects.filter(pacote=obj, status=Compra.CONFIRMADA).exists():
            return False
        return super().has_delete_permission(request, obj)


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ("nome", "pacote", "estrelas", "vagas", "ocupadas", "disponiveis", "acrescimo")
    list_editable = ("vagas", "acrescimo")
    list_filter = ("pacote", "estrelas")
    search_fields = ("nome", "pacote__nome")

    def has_delete_permission(self, request, obj=None):
        if obj and obj.ocupadas() > 0:
            return False
        return super().has_delete_permission(request, obj)


@admin.register(Compra)
class CompraAdmin(admin.ModelAdmin):
    list_display = ("destino", "usuario", "hotel_nome", "quantidade", "valor_final", "status", "data")
    list_filter = ("status", "destino", "data")
    search_fields = ("usuario__email", "usuario__first_name", "destino", "hotel_nome")
    date_hierarchy = "data"
    readonly_fields = ("data",)
    ordering = ("-data",)


@admin.register(Orcamento)
class OrcamentoAdmin(admin.ModelAdmin):
    list_display = ("nome", "email", "destino", "data_prevista", "viajantes", "criado_em", "respondido")
    list_editable = ("respondido",)
    list_filter = ("respondido", "criado_em")
    search_fields = ("nome", "email", "destino", "mensagem")
    readonly_fields = ("criado_em",)
