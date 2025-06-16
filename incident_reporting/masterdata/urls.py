from django.urls import path
from . import views

urlpatterns = [
    path('departments/', views.manage_departments, name='manage_departments'),
    path('department/edit/<int:pk>/', views.edit_department, name='edit_department'),
    path('department/delete/<int:pk>/', views.delete_department, name='delete_department'),

    path('divisions/', views.manage_divisions, name='manage_divisions'),
    path('divisions/edit/<int:pk>/', views.edit_division, name='edit_division'),
    path('divisions/delete/<int:pk>/', views.delete_division, name='delete_division'),
]