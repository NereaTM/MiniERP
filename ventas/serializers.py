from rest_framework import serializers
from core.models import Producto


class ProductoSerializer(serializers.ModelSerializer):
    # El stock no lo traemos del modelo, lo pasamos por su metodo propio
    stock = serializers.SerializerMethodField()

    class Meta:
        model = Producto
        fields = ['id_producto', 'sku', 'nombre', 'precio_base', 'stock']

    def get_stock(self, obj):
        request = self.context.get('request')
        # esta el usuario logead?
        if request and request.user.is_authenticated:
            # si - devuelve stock
            return obj.stock
        # no - devuelve null
        return None