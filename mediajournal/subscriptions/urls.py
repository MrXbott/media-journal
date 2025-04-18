from django.urls import path

from . import views

urlpatterns = [
    # path('subscribe/guest/', views.subscribe_guest, name='subscribe_guest'),
    # path('subscribe/user/', views.subscribe_user, name='subscribe_user'),
    path('subscribe/', views.subscribe, name='subscribe'),
    path('unsubscribe/', views.unsubscribe, name='unsubscribe'),

]
