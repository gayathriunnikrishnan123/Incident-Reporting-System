from django import forms
from .models import Department, Division

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'description']

class DivisionForm(forms.ModelForm):
    class Meta:
        model = Division
        fields = ['name', 'department', 'description']