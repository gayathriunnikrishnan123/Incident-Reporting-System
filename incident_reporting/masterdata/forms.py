from django import forms
from masterdata.models import Department, Division

class DepartmentForm(forms.ModelForm):
    division = forms.ModelChoiceField(
        queryset=Division.objects.filter(is_deleted=False),
        empty_label="Select Division",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    class Meta:
        model = Department
        fields = ['name', 'division', 'description']
        widgets = {
            'description': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class DivisionForm(forms.ModelForm):

    class Meta:
        model = Division
        fields = ['name','description']
        widgets = {
            'description': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }