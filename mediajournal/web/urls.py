from django.urls import path

from . import views

urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('search/', views.search, name='search'),
    path('feed/', views.user_news_feed, name='user_news_feed'),
]
