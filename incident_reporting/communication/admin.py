from django.contrib import admin

# Register your models here.
from .models import IncidentMessage, IncidentMessageAttachment

admin.site.register(IncidentMessage)
admin.site.register(IncidentMessageAttachment)