from django import forms
from .models import Department, Division

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'description']
        widgets = {
            'description': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class DivisionForm(forms.ModelForm):
    class Meta:
        model = Division
        fields = ['name', 'department', 'description']
        widgets = {
            'description': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }