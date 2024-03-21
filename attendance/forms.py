from django import forms

class AttendanceForm(forms.Form):
    status = forms.ChoiceField(choices=(
        ('present', 'Present'),
        ('absent', 'Absent'),
    ), widget=forms.RadioSelect)