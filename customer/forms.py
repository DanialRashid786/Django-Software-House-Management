import re
from django import forms
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator


from .models import *
from django.core.validators import RegexValidator
class perposalforms(forms.ModelForm):
  
    class Meta:
        model = requestform
        fields = ['project_title','phone_number','requirementfile','Project_Budget']
        widgets = {
            'project_title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Your Project Title'}),
            'requirementfile': forms.FileInput(attrs={'class': 'form-control', 'accept': '.pdf, .docx'}),
            'Project_Budget': forms.NumberInput(attrs={'step': '0.01', 'class': 'form-control', 'placeholder': 'Enter Project Budget (100.00 - 1000000.00)'}), 
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Phone Number'}), 
        }
    Project_Budget = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=100.00,
        max_value=1000000.00,
        widget=forms.NumberInput(attrs={'step': '0.01', 'class': 'form-control', 'placeholder': 'Enter Project Budget (100.00 - 1000000.00)$'}),
    )
    phone_number = forms.CharField(
        validators=[RegexValidator(r'^\+?1?\d{9,15}$', message="Enter a valid phone number.")],
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Phone Number'}),
    )
    
    requirementfile = forms.FileField(
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'docx'])],
        widget=forms.FileInput(attrs={'class': 'form-control', 'accept': '.pdf, .docx'})
    )
    def clean_requirementfile(self):
        requirementfile = self.cleaned_data.get('requirementfile')

        if requirementfile:
            # Use FileExtensionValidator to check file extension
            validator = FileExtensionValidator(allowed_extensions=['pdf', 'docx'])
            validator(requirementfile)

        return requirementfile
    
    

ProjectProposalFormSet = inlineformset_factory(Customer, requestform, form=perposalforms, extra=1, can_delete=False)




        




class CustomerForm(forms.ModelForm):
    email = forms.EmailField(required=False)
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)

    class Meta:
        model = Customer
        exclude = ['user','auth_token', 'is_verified']
    
    def save(self, commit=True):
        user = self.instance.user
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        return super(CustomerForm, self).save(commit=commit)






class PasswordChangeForm(forms.Form):
    current_password = forms.CharField(label='Current password', widget=forms.PasswordInput)
    new_password = forms.CharField(label='New password', widget=forms.PasswordInput)
    repeat_new_password = forms.CharField(label='Repeat new password', widget=forms.PasswordInput)




class RequestSessionform(forms.ModelForm):
    class Meta:
        model = RequestSession
        fields = '__all__'
        



class ProjectCompletionDocumentForm(forms.ModelForm):
    class Meta:
        model = ProjectCompletionDocument
        fields = ['document']


