from django.urls import path,include
from . import views
from .views import email_login_view
from django.contrib.auth import views as auth_views
from django.contrib import admin
from accounts.views import dashboardView, createUserView, editUserView, userListView, deleteUserView
from django.urls import path, include
from accounts.views import dashboardView, createUserView, editUserView, userListView, deleteUserView, systemConfigView, userManagementView
from django.contrib.auth.views import LoginView, LogoutView
from accounts.forms import CustomEmailLoginForm

urlpatterns = [
    path('', views.home,name='home'),
    path('dashboard/', views.dashboard,name='dashboard'),
    path('login/', email_login_view, name='login'),
    path('change-password/', views.change_password_view, name='change_password'),
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='registration/password_reset_form.html'), name='password_reset'),

    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='registration/password_reset_done.html'), name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),

    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='registration/password_reset_complete.html'), name='password_reset_complete'),


    path('login/', LoginView.as_view(template_name="registration/login.html",authentication_form=CustomEmailLoginForm),name='login'),
    path("logout/", LogoutView.as_view(next_page="home"), name='logout'),
    path('dashboard/', dashboardView, name='dashboard'),
    path('systemconfig/', systemConfigView, name='system-config'),
    path('userManagement/', userManagementView, name='user-management'),
    path('create-user/',createUserView,name='create-user'),
    path('edit-user/<int:userId>/',editUserView,name='edit-user'),
    path('delete-user/<int:userId>/',deleteUserView,name='delete-user'),
    path('all-users/',userListView,name='show-users'),
    path('admin_dashboard/',views.admin_dashboard,name='admin_dashboard'),

]
