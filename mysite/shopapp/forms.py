from django import forms

from shopapp.models import Product, Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['user', 'products', 'delivery_address', 'promocode']
        widgets = {
            'products': forms.CheckboxSelectMultiple(),
            'delivery_address': forms.Textarea(attrs={'cols': 60, 'rows': 2})
        }


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'description', 'discount',]