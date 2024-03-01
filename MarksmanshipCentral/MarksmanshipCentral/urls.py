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
    path('personal/', views.personal, name='personal'),
    path('newgame/', views.newgame, name='newgame'),
    path('newsession', views.newsession, name='newsession'),
    path('reports/', views.reports, name='reports'),
    path('oversight', views.oversight, name = 'oversight'),
    path('login/', views.login, name='login'),
    path('landing/', views.landing, name='landing'),
    path('logout/', views.logout, name='logout'),
    path('admin/', admin.site.urls),
]
