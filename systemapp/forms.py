from django import forms
from systemapp.models import Customer, Product
from .models import Invoice, InvoiceProduct, Seller
from django.forms import modelformset_factory
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'quantity', 'price']



class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'phone_number']


class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['customer', 'seller', 'phone_number']

class InvoiceProductForm(forms.ModelForm):
    class Meta:
        model = InvoiceProduct
        fields = ['product', 'quantity', 'price']

class InvoiceCreateForm(forms.ModelForm):
    product_count = forms.IntegerField(initial=0)

    class Meta:
        model = Invoice
        fields = ['customer', 'seller', 'phone_number', 'product_count']