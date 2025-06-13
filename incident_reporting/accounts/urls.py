from django.contrib import admin
from django.urls import path, include
from accounts.views import dashboardView, createUserView, editUserView, userListView, deleteUserView
from django.contrib.auth.views import LoginView, LogoutView
from accounts.forms import CustomEmailLoginForm

urlpatterns = [
    path('login/', LoginView.as_view(template_name="registration/login.html",authentication_form=CustomEmailLoginForm),name='login'),
    path("logout/", LogoutView.as_view(next_page="home"), name='logout'),
    path('dashboard/', dashboardView, name='dashboard'),
    path('create-user/',createUserView,name='create-user'),
    path('edit-user/<int:userId>/',editUserView,name='edit-user'),
    path('delete-user/<int:userId>/',deleteUserView,name='delete-user'),
    path('all-users/',userListView,name='show-users'),
]