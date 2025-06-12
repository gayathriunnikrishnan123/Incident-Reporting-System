from django.contrib import admin
from django.urls import path, include
from accounts.views import loginView, dashboardView, createUserView, editUserView, userListView, deleteUserView

urlpatterns = [
    path('login/', loginView,name='login'),
    path('dashboard/', dashboardView, name='dashboard'),
    path('create-user/',createUserView,name='create-user'),
    path('edit-user/<int:userId>/',editUserView,name='edit-user'),
    path('delete-user/<int:userId>/',deleteUserView,name='delete-user'),
    path('all-users/',userListView,name='show-users'),
]