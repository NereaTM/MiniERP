from django.contrib import admin
from .models import Oportunidad

@admin.register(Oportunidad)
class OportunidadAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'cliente', 'etapa', 'valor_estimado', 'dias_abierta', 'fecha_creacion')
    list_filter = ('etapa',)
    search_fields = ('titulo', 'cliente__nombre')
    readonly_fields = ('fecha_creacion', 'dias_abierta')