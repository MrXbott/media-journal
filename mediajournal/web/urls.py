from django.urls import path

from . import views

urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('search/', views.search, name='search'),
    path('feed/', views.subscriptions_feed, name='subscriptions_feed'),
]
