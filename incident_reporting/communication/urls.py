from django.urls import path
from .views import incident_chat_view, post_chat_message

urlpatterns = [
    path('incident/<int:incident_id>/chat/', incident_chat_view, name='incident_chat'),
    path('incident/<int:incident_id>/send-message/', post_chat_message, name='post_chat_message'),
]
