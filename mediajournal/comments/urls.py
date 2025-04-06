from django.urls import path, register_converter

from . import views

urlpatterns = [
    path('comment/', views.post_comment, name='post_comment'),
    path('comments/', views.comments_list, name='comments_list'),
]
