from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from customer.models import projectmanagers

from .models import *

class projectmanagerForm(ModelForm):
    # email = forms.EmailField(required=False)
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    class Meta:
        model = projectmanagers
        fields = '__all__'
        exclude = ['user','job','company']
    
    def save(self, commit=True):
        user = self.instance.user
        # user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        return super().save(commit=commit)




class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']







class projectteam(UserCreationForm): 
    
    team_type = forms.ChoiceField(choices=Team.team_type_choices)

    company = forms.CharField(label='company')
    country = forms.CharField(label='country')
    

    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'email', 'first_name', 'last_name','team_type', 'team_type','company', 'country')

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Invalid Email')
        return email   



class TaskFilterForm(forms.Form):
    project = forms.ChoiceField(choices=[], required=False)
    team_member = forms.ChoiceField(choices=[], required=False)
    status = forms.ChoiceField(choices=[('', 'All'), ('todo', 'To Do'), ('in_progress', 'In Progress'), ('completed', 'Completed'),('to_review','To Review'),("needs_revision", "Needs Revision")], required=False)
    
