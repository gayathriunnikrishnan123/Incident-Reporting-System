from django import forms
from .models import IncidentMessage, IncidentMessageAttachment

class IncidentMessageForm(forms.ModelForm):
    class Meta:
        model = IncidentMessage
        fields = ['message', 'is_internal']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Type your message...'}),
        }

class IncidentMessageAttachmentForm(forms.ModelForm):
    class Meta:
        model = IncidentMessageAttachment
        fields = ['file']
