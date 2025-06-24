from django.shortcuts import render
from accounts.decorators import audit_trail_decorator
# Create your views here.

@audit_trail_decorator
def homePage(request):
    return render(request,'home.html')


@audit_trail_decorator
def incidentHomePage(request):
    return render(request,'incidentHome.html')