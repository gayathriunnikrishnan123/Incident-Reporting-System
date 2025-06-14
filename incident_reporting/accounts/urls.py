from django.contrib import admin
from django.urls import path, include
from accounts import views
from django.contrib.auth.views import LoginView, LogoutView
from accounts.forms import CustomEmailLoginForm

urlpatterns = [
    path('login/', LoginView.as_view(template_name="registration/login.html",authentication_form=CustomEmailLoginForm),name='login'),
    path("logout/", LogoutView.as_view(next_page="home"), name='logout'),

    path('dashboard/', views.dashboardView, name='dashboard'),
    path('systemconfig/', views.systemConfigView, name='system-config'),
    path('userManagement/', views.userManagementView, name='user-management'),

    path('create-user/',views.createUserView,name='create-user'),
    path('edit-user/<int:userId>/',views.editUserView,name='edit-user'),
    path('delete-user/<int:userId>/',views.deleteUserView,name='delete-user'),
    path('all-users/',views.userListView,name='show-users'),

    path('roles/',views.roleView,name='show-roles'),
    path('edit-role/<int:roleId>/',views.editRoleView,name='edit-role'),
    path('delete-role/<int:roleId>/',views.deleteRoleView,name='delete-role'),


    path('auditlog/',views.auditLogView,name='auditlog'),


    path('mappings/',views.departmentProfileView,name='show-maps'),
    path('edit-map/<int:mapId>/',views.departmentProfileEditView,name='edit-map'),
    path('delete-map/<int:mapId>/',views.departmentProfileDeleteView,name='delete-map'),
]