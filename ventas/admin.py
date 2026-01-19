from django.contrib import admin
from .models import Pedido, LineaPedido


class LineaPedidoInline(admin.TabularInline):
    model = LineaPedido
    extra = 1
    fields = ["producto", "descripcion", "cantidad", "precio_unitario", "tipo_iva"]


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ["id_pedido", "cliente", "estado_pedido", "fecha_pedido", "total_neto"]
    list_filter = ["estado_pedido", "fecha_pedido"]
    search_fields = ["cliente__nombre", "cliente__nif"]
    date_hierarchy = "fecha_pedido"
    ordering = ["-fecha_pedido", "-id_pedido"]
    inlines = [LineaPedidoInline]


@admin.register(LineaPedido)
class LineaPedidoAdmin(admin.ModelAdmin):
    list_display = ["id_linea_pedido", "pedido", "producto", "cantidad", "precio_unitario", "tipo_iva"]
    list_filter = ["pedido__estado_pedido"]
    search_fields = ["pedido__id_pedido", "producto__sku", "producto__nombre", "descripcion"]
    ordering = ["-pedido__fecha_pedido", "-id_linea_pedido"]
