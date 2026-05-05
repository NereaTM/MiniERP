from django.db import models
from django.db.models import Q, CheckConstraint
from django.utils import timezone
from core.models import Cliente, Producto, EstadoPedido
from decimal import Decimal
from django.core.exceptions import ValidationError


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

    class Meta:
        db_table = "Pedido"

    def __str__(self):
        return f"Pedido #{self.id_pedido} - {self.cliente.nombre}"

    # VALIDACIÓN ANTES DE GUARDAR
    def clean(self):
        if self.estado_pedido.nombre == "CONFIRMADO":
            for linea in self.lineas.all():
                if linea.producto.stock < int(linea.cantidad):
                    raise ValidationError(
                        f"No hay stock suficiente para {linea.producto.nombre}"
                    )

    # validación en el admin 
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    # CÁLCULO DE TOTALES
    def calcular_totales(self):
        lineas = self.lineas.all()

        base = Decimal("0.00")
        iva = Decimal("0.00")

        for linea in lineas:
            subtotal = linea.precio_unitario * linea.cantidad
            base += subtotal
            iva += subtotal * linea.tipo_iva

        self.total_bruto = base
        self.total_iva = iva
        self.total_neto = base + iva

        super().save(update_fields=["total_bruto", "total_iva", "total_neto"])


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

        # recalcular totales automáticamente
        self.pedido.calcular_totales()

    def delete(self, *args, **kwargs):
        pedido = self.pedido
        super().delete(*args, **kwargs)

        # recalcular tras borrar
        pedido.calcular_totales()

    def __str__(self):
        return f"{self.descripcion} x{self.cantidad}"