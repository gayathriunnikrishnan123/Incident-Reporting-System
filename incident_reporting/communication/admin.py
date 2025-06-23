from django.contrib import admin
from .models import IncidentMessage, IncidentMessageAttachment

admin.site.register(IncidentMessage)
admin.site.register(IncidentMessageAttachment)