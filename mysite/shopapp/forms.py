from django import forms
from django.contrib.auth.models import Group
from shopapp.models import Product, Order


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name']


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['user', 'products', 'delivery_address', 'promocode']
        widgets = {
            'products': forms.CheckboxSelectMultiple(),
            'delivery_address': forms.Textarea(attrs={'cols': 60, 'rows': 2})
        }


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleImageField(forms.ImageField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'description', 'discount',]

    images = MultipleImageField()


class CSVImportForm(forms.Form):
    csv_file = forms.FileField()

