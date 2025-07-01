from django import forms
from .models import IncidentMessage, IncidentMessageAttachment

class IncidentMessageFormPublic(forms.ModelForm):
    class Meta:
        model = IncidentMessage
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={
                'class': 'form-control textarea',
                'rows': 3,
                'placeholder': 'Type your message...',
            }),
        }

class IncidentMessageFormInternal(forms.ModelForm):
    class Meta:
        model = IncidentMessage
        fields = ['message', 'is_internal_only']
        widgets = {
            'message': forms.Textarea(attrs={
                'class': 'form-control textarea',
                'rows': 3,
                'placeholder': 'Enter your response...',
            }),
            'is_internal_only': forms.CheckboxInput()
        }

class IncidentMessageAttachmentForm(forms.ModelForm):
    file = forms.FileField(
        required=False,
        widget=forms.FileInput(attrs={'multiple': True}),
        label="Attach files (optional)"
    )
    class Meta:
        model = IncidentMessageAttachment
        fields = ['file']
        