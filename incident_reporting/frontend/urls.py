from django.urls import path
from frontend.views import homePage,incidentHomePage


urlpatterns = [
    path('',incidentHomePage,name='inc-home'),
    path('internals/',homePage,name='home'),
]
