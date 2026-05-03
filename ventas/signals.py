from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from .models import Pedido
import logging

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Pedido)
def actualizar_stock(sender, instance, created, **kwargs):
    """
    Cuando un pedido pasa a CONFIRMADO:
    - Resta stock de productos
    - Valida que haya stock suficiente
    """

    if created:
        return # es un pedido nuevo, no hace nada

    if instance.estado_pedido.nombre != "CONFIRMADO":
        return  # solo actúa si el estado es CONFIRMADO

    # recorre las lineas para comprobar si hay stock
    for linea in instance.lineas.all():
        producto = linea.producto

        if producto.stock < linea.cantidad:
            logger.error(f"No hay stock suficiente para {producto.nombre}")

            raise ValidationError(
                f"No hay stock suficiente para {producto.nombre}"
            )

        # Restar stock
        producto.stock -= linea.cantidad
        producto.save()