from django.urls import path
from frontend.views import homePage


urlpatterns = [
    path('',homePage,name='home'),
]
