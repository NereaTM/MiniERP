from django.db import models
from django.db.models import Q, CheckConstraint
from django.utils import timezone
from core.models import Cliente, Producto, EstadoPedido


class Pedido(models.Model):
    id_pedido = models.AutoField(primary_key=True, db_column="id_pedido")

    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.RESTRICT, # No se puede borrar cliente con pedidos
        db_column="id_cliente",
        related_name="pedidos",
    )

    estado_pedido = models.ForeignKey(
        EstadoPedido,
        on_delete=models.RESTRICT, # No se puede borrar estado en uso
        db_column="id_estado_pedido",
        default=1,
        related_name="pedidos",
    )
    
    # auto-rellenar
    fecha_pedido = models.DateTimeField(default=timezone.now)

    total_bruto = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_iva = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_neto = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "Pedido"
        indexes = [
            models.Index(fields=["cliente", "fecha_pedido"], name="idx_pedido_cliente_fecha"),
            models.Index(fields=["cliente"], name="idx_pedido_cliente_top"),
        ]

    def __str__(self):
        return f"Pedido #{self.id_pedido} - {self.cliente.nombre}"
    
    def calcular_totales(self):
        lineas = self.lineas.all()
        
        self.total_bruto = sum(linea.cantidad * linea.precio_unitario for linea in lineas)
        self.total_iva = sum(linea.cantidad * linea.precio_unitario * linea.tipo_iva for linea in lineas )
        
        self.total_neto = self.total_bruto + self.total_iva
        self.save()

class LineaPedido(models.Model):
    id_linea_pedido = models.AutoField(primary_key=True, db_column="id_linea_pedido")

    pedido = models.ForeignKey(
        Pedido,
        on_delete=models.CASCADE, # Si borro pedido, borro líneas
        db_column="id_pedido",
        related_name="lineas",
    )

    producto = models.ForeignKey(
        Producto,
        on_delete=models.RESTRICT, # No se puede borrar producto en uso
        db_column="id_producto",
        related_name="lineas_pedido",
    )
    
    # SNAPSHOT
    descripcion = models.CharField(max_length=255)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    tipo_iva = models.DecimalField(max_digits=4, decimal_places=2)

    class Meta:
        db_table = "LineaPedido"

        constraints = [
            CheckConstraint(
                condition=Q(cantidad__gt=0),
                name="check_cantidad_positiva"
            )
        ]

    def save(self, *args, **kwargs):
            # Auto-relleno snapshots
            if self.descripcion in (None, ""):
                self.descripcion = self.producto.nombre
            if self.precio_unitario is None:
                self.precio_unitario = self.producto.precio_base
            if self.tipo_iva is None:
                self.tipo_iva = self.producto.tipo_iva
            super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.descripcion} x{self.cantidad} (Pedido #{self.pedido_id})"
