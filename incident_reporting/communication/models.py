from django.db import models
from django.conf import settings
from incidents.models import Incident

class IncidentMessage(models.Model):
    incident = models.ForeignKey(Incident, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    message = models.TextField()
    is_internal = models.BooleanField(default=False)  
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message on {self.incident.incident_token} by {self.sender or 'Anonymous'}"


class IncidentMessageAttachment(models.Model):
    message = models.ForeignKey(IncidentMessage, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='incident_message_attachments/')
    uploaded_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Attachment for Message {self.message.id}"
