"""
Definition of urls for MarksmanshipCentral.
"""

from datetime import datetime
from django.urls import path
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from app import views, ajaxviews



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
    path('registration/', views.registration, name='registration'),
    path('test/',views.test,name='test'),
    path('admin/', admin.site.urls),
    path('game_autocomplete/', ajaxviews.game_autocomplete, name='game_autocomplete'),
    path('game_autocomplete/full/', ajaxviews.librarysearch_autocomplete, name='librarysearch_autocomplete'),
    path('member_autocomplete/', ajaxviews.member_autocomplete, name='member_autocomplete'),
    path('game_approve/', ajaxviews.game_approve, name='approve_game'),
    path('game_replace/', ajaxviews.game_replace, name='replace_game'),
    path('game_save/', ajaxviews.game_save, name='save_game'),
    path('game_delete/', ajaxviews.game_delete, name='delete_game'),
    path('session_resolve/', ajaxviews.session_resolve, name='resolve_session'),
    path('session_replace/', ajaxviews.session_replace, name='replace_session'),
    path('fleet_chapters/', ajaxviews.fleet_chapters, name='fleet_chapters'),
    path('reports/member/', views.member_reports, name='member-reports'),
    path('reports/credit/', views.credit_reports, name='credit-reports'),
    path('reports/award/', views.award_reports, name='award-reports'),
    path('data-csv', views.data_csv, name='data-csv'),
]
