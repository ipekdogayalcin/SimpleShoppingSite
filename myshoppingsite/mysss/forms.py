from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms
from .models import Product, Purchase
from django.contrib.auth.models import User

class PurchaseForm(forms.ModelForm):
    shipping_address = forms.CharField(max_length=255, required=True, widget=forms.TextInput(attrs={'placeholder': 'Shipping Address'}))
    card_credentials = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={'placeholder': 'Card Credentials'}))
    cvc = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={'placeholder': 'CVC'}))
    expiry_month = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={'placeholder': 'MM'}))
    expiry_year = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={'placeholder': 'YY'}))

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['products'] = forms.ModelMultipleChoiceField(queryset=user.customer.cart.all(), required=True)

    class Meta:
        model = Purchase
        fields = ['shipping_address', 'card_credentials', 'cvc', 'expiry_month', 'expiry_year']


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['item_type', 'color', 'material', 'stock', 'image_url', 'price']
        widgets = {
            'item_type': forms.TextInput(attrs={'placeholder': 'Item Type'}),
            'color': forms.TextInput(attrs={'placeholder': 'Color'}),
            'material': forms.TextInput(attrs={'placeholder': 'Material'}),
            'stock': forms.NumberInput(attrs={'placeholder': 'Stock'}),
            'image_url': forms.URLInput(attrs={'placeholder': 'Image URL'}),
            'price': forms.NumberInput(attrs={'placeholder': 'Price'}),
        }

