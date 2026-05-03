from django.db import models
from django.utils import timezone
from core.models import Cliente

class Oportunidad(models.Model):
    class Etapa(models.TextChoices):
        PROSPECCION = 'PRO', 'Prospección'
        PROPUESTA = 'PRP', 'Propuesta'
        NEGOCIACION = 'NEG', 'Negociación'
        GANADA = 'GAN', 'Cerrada Ganada'
        PERDIDA = 'PER', 'Cerrada Perdida'

    titulo = models.CharField(max_length=200)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='oportunidades')
    valor_estimado = models.DecimalField(max_digits=12, decimal_places=2)
    etapa = models.CharField(max_length=3, choices=Etapa.choices, default=Etapa.PROSPECCION)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_cierre = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.titulo} — {self.cliente}"

    @property
    def dias_abierta(self):
        if not self.fecha_creacion:
            return 0
        final = self.fecha_cierre if self.fecha_cierre else timezone.now()
        return (final - self.fecha_creacion).days

    @property
    def esta_cerrada(self):
        return self.etapa in (self.Etapa.GANADA, self.Etapa.PERDIDA)

    class Meta:
        verbose_name = 'Oportunidad'
        verbose_name_plural = 'Oportunidades'
        ordering = ['-fecha_creacion']