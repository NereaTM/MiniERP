from django.shortcuts import render
from .models import Oportunidad

def crm_dashboard(request):
    oportunidades = Oportunidad.objects.select_related('cliente').all()

    total = oportunidades.count()
    ganadas = oportunidades.filter(etapa=Oportunidad.Etapa.GANADA).count()
    tasa_conversion = round(ganadas / total * 100, 2) if total > 0 else 0

    context = {
        'tasa_conversion': tasa_conversion,
        'total': total,
        'ganadas': ganadas,
        'oportunidades': oportunidades.order_by('-valor_estimado'),
        'moneda': '€',
    }
    return render(request, 'crm/dashboard.html', context)