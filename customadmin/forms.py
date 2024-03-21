from django import forms  
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm  
from django.core.exceptions import ValidationError  
from django.forms.fields import EmailField  
from django.forms.forms import Form

from customer.models import Career, services


  
class CustomUserCreationForm(UserCreationForm): 
    company = forms.CharField(label='company')
    job = forms.CharField(label='job')
    country = forms.CharField(label='country')

    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'email', 'first_name', 'last_name', 'company','job', 'country')

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Invalid Email')
        return email    




# class ChangePasswordForm(forms.Form):
#     password = forms.CharField(widget=forms.PasswordInput())
    
class CareerFormdata(forms.ModelForm):
    class Meta:
        model = Career
        fields = '__all__'
#         exclude = ['RequestStatus']
        


class ServiceForm(forms.ModelForm):
    class Meta:
        model = services
        fields = '__all__'
    