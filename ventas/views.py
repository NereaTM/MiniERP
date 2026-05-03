from rest_framework.generics import ListAPIView
from core.models import Producto
from .serializers import ProductoSerializer
from rest_framework.permissions import IsAuthenticated

class ProductoListAPIView(ListAPIView):
    queryset = Producto.objects.all().order_by('id_producto')
    serializer_class = ProductoSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context