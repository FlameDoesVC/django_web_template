from django import forms 
from django.contrib.auth.forms import UserCreationForm
from .models import User, CartItem

class SignupForm(UserCreationForm):
    class Meta:
        model = User 
        fields = ['username', 'password1', 'password2']

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class CartItemForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = ['product', 'size', 'color', 'quantity']
        widgets = {
            'product': forms.HiddenInput(),
            'size': forms.Select(),
            'color': forms.Select(),
            'quantity': forms.NumberInput(),
        }