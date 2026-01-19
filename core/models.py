from django.db import models


class Cliente(models.Model):
    id_cliente = models.AutoField(primary_key=True, db_column="id_cliente")
    nombre = models.CharField(max_length=255)
    nif = models.CharField(max_length=30, unique=True)
    direccion = models.TextField(blank=True, null=True)
    email = models.CharField(max_length=255, unique=True, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "Cliente"

    def __str__(self):
        return f"{self.nombre} ({self.nif})"


class Producto(models.Model):
    id_producto = models.AutoField(primary_key=True, db_column="id_producto")
    sku = models.CharField(max_length=100, unique=True)
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True, null=True)
    precio_base = models.DecimalField(max_digits=10, decimal_places=2)
    tipo_iva = models.DecimalField(max_digits=4, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "Producto"

    def __str__(self):
        return f"{self.sku} - {self.nombre}"
    
    def precio_con_iva(self):
        """Calcula el precio con IVA incluido"""
        return self.precio_base * (1 + self.tipo_iva)



class EstadoPedido(models.Model):
    id_estado_pedido = models.AutoField(primary_key=True, db_column="id_estado_pedido")
    nombre = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = "EstadoPedido"


    def __str__(self):
        return self.nombre
