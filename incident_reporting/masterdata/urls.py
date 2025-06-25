from django.urls import path
from . import views

urlpatterns = [
    path('departments/', views.manage_departments, name='manage_departments'),
    path('department/edit/<int:pk>/', views.edit_department, name='edit_department'),
    path('department/delete/<int:pk>/', views.delete_department, name='delete_department'),

    path('divisions/', views.manage_divisions, name='manage_divisions'),
    path('divisions/edit/<int:pk>/', views.edit_division, name='edit_division'),
    path('divisions/delete/<int:pk>/', views.delete_division, name='delete_division'),

    path('severities/', views.manage_severity, name='manage_severity'),
    path('severities/edit/<int:pk>/', views.edit_severity, name='edit_severity'),
    path('severities/delete/<int:pk>/', views.delete_severity, name='delete_severity'),

    path('status/', views.manage_status, name='manage_status'),
    path('status/edit/<int:pk>/', views.edit_status, name='edit_status'),
    path('status/delete/<int:pk>/', views.delete_status, name='delete_status'),

    path('role-status-mapping/', views.role_status_mapping_view, name='role-status-mapping'),
    path('role-status-mapping/edit/<int:pk>/', views.edit_role_status_mapping, name='edit-role-status-mapping'),
    path('delete-role-status-mapping/<int:pk>/', views.delete_role_status_mapping, name='delete-role-status-mapping'),
]