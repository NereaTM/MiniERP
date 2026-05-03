from django import forms
from core.models import Producto, Cliente


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['sku', 'nombre', 'precio_base', 'tipo_iva', 'stock']

    def clean_stock(self):
        stock = self.cleaned_data.get('stock')
        if stock < 0:
            raise forms.ValidationError("El stock no puede ser negativo")
        return stock


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'nif', 'direccion', 'email']

    def clean_nif(self):
        nif = self.cleaned_data.get('nif')
        # El NIF/CIF debe ser único 
        qs = Cliente.objects.filter(nif=nif)
        # Si editamos lo excluimos
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("Ya existe un cliente con este NIF/CIF")
        return nif

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            return email
        if '@' not in email or '.' not in email.split('@')[-1]:
            raise forms.ValidationError("Introduce un email válido")
        return email