from django import forms
from .models import Asset

class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ['asset_type','asset_name', 'purchase_date', 'purchase_price', 'serial_number', 'notes']

        widgets = {
            'purchase_date': forms.DateInput(attrs={'type': 'date'}),
        }




class updatedata(forms.ModelForm):
    class Meta:
        model = Asset
        fields = '__all__'
        widgets = {
            'purchase_date': forms.DateInput(attrs={'type': 'date'}),
        }