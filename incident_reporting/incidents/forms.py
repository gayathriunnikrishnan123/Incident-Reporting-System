from django import forms
from incidents.models import Incident

class IncidentForm(forms.ModelForm):
    class Meta:
        model = Incident
        fields = [
            'title',
            'description',
            'division',
            'department',
            'priority',
            'email',
            'phone',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter incident title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Describe the issue'}),
            'division': forms.Select(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-control'}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Optional'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Optional'}),
        }
        labels = {
            'title': 'Incident Title',
            'description': 'Description',
            'division': 'Select Division (optional)',
            'department': 'Select Department (optional)',
            'priority': 'Priority (optional)',
            'email': 'Your Email (optional)',
            'phone': 'Your Phone (optional)',
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone and not phone.isdigit():
            raise forms.ValidationError("Phone number should contain digits only.")
        return phone
