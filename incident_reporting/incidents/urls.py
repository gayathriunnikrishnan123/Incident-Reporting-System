from django.urls import path
from incidents import views

urlpatterns = [
    path('report/', views.submit_incident, name='submit_incident'),
    path('get-report/',views.track_incident_by_token,name='get_incidentby_token'),
    path('success/<str:token>/', views.incident_success, name='incident_success'),
]