from django.urls import path
from incidents import views

urlpatterns = [
    path('submit/', views.submit_incident, name='submit_incident'),
    path('success/<str:token>/', views.incident_success, name='incident_success'),
]