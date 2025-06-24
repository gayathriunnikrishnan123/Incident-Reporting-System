from django.urls import path
from communication import views


urlpatterns = [

    path('public-chat/<str:token>/', views.ajax_public_chat, name='ajax_public_chat'),
    path('internal-chat/<str:token>/', views.ajax_internal_chat, name='ajax_internal_chat'),
]
