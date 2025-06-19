from django.urls import path
from incidents import views

urlpatterns = [
    path('report/', views.submit_incident, name='submit_incident'),
    path('success/<str:token>/', views.incident_success, name='incident_success'),
    path('get-report/',views.track_incident_by_token,name='get_incidentby_token'),
    path('get-report-details/<str:token>/',views.incident_details_by_token,name='detailsby_token'),
]