from django.db import models
import uuid
from django.utils import timezone
from masterdata.models import Division, Department, IncidentStatus, IncidentSeverity
from accounts.models import CustomUserProfile
# Create your models here.

def generate_incident_token():
    return f"INC-{timezone.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}"

class Incident(models.Model):

    # INCIDENT_STATUS_CHOICES = [
    #     ('New', 'New'),
    #     ('Assigned', 'Assigned'),
    #     ('Escalated', 'Escalated'),
    #     ('Transferred', 'Transferred'),
    #     ('Closed', 'Closed'),
    # ]

    title = models.CharField(max_length=255)
    description = models.TextField()

    division = models.ForeignKey(Division, on_delete=models.SET_NULL, null=True,blank=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)

    status = models.ForeignKey(IncidentStatus,on_delete=models.SET_NULL,null=True, blank=True)
    priority = models.ForeignKey(IncidentSeverity,on_delete=models.SET_NULL,null=True, blank=True)


    assigned_to = models.ForeignKey(CustomUserProfile, null=True, blank=True, on_delete=models.SET_NULL, related_name='assigned_incidents')

    
    manually_assigned = models.BooleanField(default=False)
    
    incident_token = models.CharField(max_length=50, unique=True, default=generate_incident_token)

    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
