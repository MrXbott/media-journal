from django.urls import path, register_converter

from . import views

urlpatterns = [
    path('', views.get_all_news, name='all_news'),
    path('<int:news_id>/', views.get_one_news, name='one_news'),
    path('suggest/', views.suggest_news, name='suggest_news'),
]
