from django.urls import path, register_converter

from . import views


urlpatterns = [
    path('bookmark/', views.add_remove_bookmark, name='add_remove_bookmark'),
]