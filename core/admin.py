from django.contrib import admin
from django import forms

<<<<<<< HEAD
from .models import Compra, Hotel, Orcamento, Pacote


class HotelInline(admin.TabularInline):
=======
from .models import Compra, Orcamento, Pacote, Hotel

class HotelInline(admin.StackedInline):
>>>>>>> 1c8228b5a3fb9d6ec982ed510696cfa6d2fb7eb7
    model = Hotel
    extra = 1


@admin.register(Pacote)
class PacoteAdmin(admin.ModelAdmin):
    list_display = ("nome", "preco", "ativo", "no_carrossel", "ordem", "hoteis_cadastrados")
    list_editable = ("preco", "ativo", "no_carrossel", "ordem")
    list_filter = ("ativo", "no_carrossel")
    search_fields = ("nome", "descricao")
<<<<<<< HEAD
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
=======
    ordering = ("nome","ordem")

    def has_delete_permission(self, request, obj=None):
        if obj and Compra.objects.filter(
                pacote=obj,
                status=Compra.CONFIRMADA
        ).exists():
            return False

>>>>>>> 1c8228b5a3fb9d6ec982ed510696cfa6d2fb7eb7
        return super().has_delete_permission(request, obj)


@admin.register(Compra)
class CompraAdmin(admin.ModelAdmin):
<<<<<<< HEAD
    list_display = ("destino", "usuario", "hotel_nome", "quantidade", "valor_final", "status", "data")
    list_filter = ("status", "destino", "data")
    search_fields = ("usuario__email", "usuario__first_name", "destino", "hotel_nome")
    date_hierarchy = "data"
    readonly_fields = ("data",)
    ordering = ("-data",)
=======
    list_display = ("destino", "usuario", "quantidade", "valor_original",
                    "desconto_percentual", "valor_final", "data", "status")
    list_filter = ("destino", "data" , "status")
    search_fields = ("usuario__email", "usuario__first_name", "destino", "hotel_nome")
    date_hierarchy = "data"
    readonly_fields = ("data",)
    ordering = ("data",)
>>>>>>> 1c8228b5a3fb9d6ec982ed510696cfa6d2fb7eb7


@admin.register(Orcamento)
class OrcamentoAdmin(admin.ModelAdmin):
    list_display = ("nome", "email", "destino", "data_prevista", "viajantes", "criado_em", "respondido")
    list_editable = ("respondido",)
    list_filter = ("respondido", "criado_em")
    search_fields = ("nome", "email", "destino", "mensagem")
    readonly_fields = ("criado_em",)
    ordering = ("-criado_em",)

class HotelAdminForm(forms.ModelForm):

    class Meta:
        model = Hotel
        fields = "__all__"

    def clean_vagas(self):
        vagas = self.cleaned_data["vagas"]

        if self.instance.pk:
            ocupadas = self.instance.ocupadas()

            if vagas < ocupadas:
                raise forms.ValidationError(
                    f"Já existem {ocupadas} vaga(s) confirmadas. "
                    "A capacidade não pode ser menor que a ocupação."
                )

        return vagas



@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ("nome", "pacote", "estrelas", "vagas", "ocupadas_", "livres_", "acrescimo")
    list_editable = ("vagas", "acrescimo")
    list_filter = ("pacote",)
    search_fields = ("nome", "pacote__nome")
    ordering = ("nome",)

    def has_delete_permission(self, request, obj=None):
        if obj and obj.ocupadas() > 0:
            return False

        return super().has_delete_permission(request, obj)

    @admin.display(description="Vagas ocupadas")
    def ocupadas_(self, obj):
        return obj.ocupadas()

    @admin.display(description="Vagas disponíveis")
    def livres_(self, obj):
        return obj.disponiveis()