from django.contrib import admin
from django.urls import path, include
from accounts import views
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import views as auth_views
from accounts.forms import CustomEmailLoginForm

urlpatterns = [
    path('login/', LoginView.as_view(template_name="registration/login.html",authentication_form=CustomEmailLoginForm),name='login'),
    path('logout/', LogoutView.as_view(next_page="home"), name='logout'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='registration/password_change_form.html'), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'), name='password_change_done'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html',email_template_name='registration/password_reset_email.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),



    path('dashboard/', views.dashboardView, name='dashboard'),
    path('systemconfig/', views.systemConfigView, name='system-config'),
    path('userManagement/', views.userManagementView, name='user-management'),

    path('create-user/',views.createUserView,name='create-user'),
    path('ajax/get-departments/', views.get_departments_by_division, name='ajax-get-departments'),
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