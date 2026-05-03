from django.urls import path
from .views import ProductoListAPIView

urlpatterns = [
    path('api/productos/', ProductoListAPIView.as_view(), name='api_productos'),
]