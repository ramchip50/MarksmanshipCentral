"""
Definition of urls for MarksmanshipCentral.
"""

from datetime import datetime
from django.urls import path
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from app import forms, views


urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('login/', views.login, name='login'),
    path('landing/', views.landing, name='landing'),
    path('logout/', views.logout, name='logout'),
    path('admin/', admin.site.urls),
]
