from django.urls import path
from . import views

urlpatterns = [
    path('department/', views.manage_departments, name='manage_departments'),
    path('divisions/', views.manage_divisions, name='manage_divisions'),
]