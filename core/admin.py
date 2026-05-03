from django.contrib import admin
from .models import Cliente, Producto, EstadoPedido

from ventas.forms import ProductoForm, ClienteForm


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    form = ClienteForm

    list_display = ["nif", "nombre", "email", "direccion"]
    search_fields = ["nif", "nombre", "email"]
    ordering = ["nombre"]


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    form = ProductoForm 
    
    list_display = ["sku", "nombre", "precio_base", "tipo_iva", "stock"]
    search_fields = ["sku", "nombre"]
    ordering = ["nombre"]


@admin.register(EstadoPedido)
class EstadoPedidoAdmin(admin.ModelAdmin):
    list_display = ["id_estado_pedido", "nombre"]
    search_fields = ["nombre"]
    ordering = ["id_estado_pedido"]