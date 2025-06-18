from django.urls import path
from frontend.views import *


urlpatterns = [
    path('',homePage,name='home'),
    path('incidentHome/',IncidenthomePage,name="incidenthome"),
]
