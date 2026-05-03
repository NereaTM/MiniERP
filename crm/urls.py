from django.urls import path
from .views import crm_dashboard

urlpatterns = [
    path('', crm_dashboard, name='crm_dashboard'),
]