from django import forms
from incidents.models import Incident, IncidentSeverity, IncidentStatus
from masterdata.models import Division


class IncidentForm(forms.ModelForm):
    file = forms.FileField(
        required=False,
        widget=forms.FileInput(attrs={'multiple': True}),
        label="Attach files (optional)"
    )
    division = forms.ModelChoiceField(
        queryset=Division.objects.filter(is_deleted=False),
        empty_label="Select Division",
        required=False,
        widget=forms.Select()
    )

    priority=forms.ModelChoiceField(
        queryset=IncidentSeverity.objects.filter(is_deleted=False),
        empty_label="Select Severity",
        required=False,
        widget=forms.Select()
    )
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
            'title': forms.TextInput(attrs={'placeholder': 'Enter incident title'}),
            'description': forms.Textarea(attrs={'placeholder': 'Describe the issue'}),
            'department': forms.Select(),
            'email': forms.EmailInput(attrs={'placeholder': 'Optional'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Optional'}),
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






class IncidentStatusUpdateForm(forms.ModelForm):
    status = forms.ModelChoiceField(
        queryset=IncidentStatus.objects.filter(is_deleted=False),
        empty_label="Select Status",
        required=True,
        widget=forms.Select())
    class Meta:
        model = Incident
        fields = ['status']
