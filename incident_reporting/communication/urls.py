from django.urls import path
from .views import incident_chat_view

urlpatterns = [
    path('incident/<int:incident_id>/chat/', incident_chat_view, name='incident_chat'),
]
