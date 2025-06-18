from django import forms

class IncidentReportForm(forms.Form):
    title = forms.CharField(max_length=200, label='Incident Title')
    description = forms.CharField(widget=forms.Textarea, label='Description')
    location = forms.CharField(max_length=200, label='Location')
    department = forms.CharField(max_length=100, label='Department')
    division = forms.CharField(max_length=100, label='Division')
    email = forms.EmailField(required=False, label='Email (Optional)')
    phone = forms.CharField(max_length=15, required=False, label='Phone Number (Optional)')
    attachments = forms.FileField(required=False, widget=forms.ClearableFileInput(attrs={'multiple': True}), label='Attachments')

