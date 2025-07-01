from django.db import models
from accounts.models import CustomUserProfile
from incidents.models import Incident
# Create your models here.


class IncidentMessage(models.Model):
    incident = models.ForeignKey(Incident, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(CustomUserProfile, on_delete=models.SET_NULL, null=True, blank=True)
    message = models.TextField()
    is_internal_only = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message by {self.sender or 'Anonymous'} on {self.created_at.strftime('%Y-%m-%d %H:%M')}"

class IncidentMessageAttachment(models.Model):
    message = models.ForeignKey(IncidentMessage, on_delete=models.CASCADE, related_name='msgAttachments')
    file = models.FileField(upload_to='message_attachments/')
    uploaded_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Attachment for message ID {self.message.id}"
