from django import forms
from django.contrib.auth.forms import PasswordResetForm

class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        max_length=254,
        widget=forms.EmailInput(attrs={'autocomplete': 'email', 'class': 'form-control' ,'placeholder': 'Enter your email'}),
        label='',
    )