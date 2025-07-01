from django.contrib import admin

# Register your models here.
from .models import IncidentQuestion, IncidentAnswer

admin.site.register(IncidentQuestion)
admin.site.register(IncidentAnswer)