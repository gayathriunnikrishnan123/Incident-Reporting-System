from django.urls import path
from .views import report_incident
from django.views.generic import TemplateView


urlpatterns = [
    path('report/', report_incident, name='report_incident'),
    path('view-incident/', TemplateView.as_view(template_name='check_token.html'), name='view_incident'),

]