from django.shortcuts import render
from accounts.decorators import audit_trail_decorator
# Create your views here.

@audit_trail_decorator
def homePage(request):
    return render(request,'home.html')


@audit_trail_decorator
def IncidenthomePage(request):
    return render(request,'Incidenthome.html')