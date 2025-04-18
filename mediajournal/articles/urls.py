from django.urls import path, register_converter

from . import views
from .converters import CustomSlugConverter

register_converter(CustomSlugConverter, 'cstmslug')

urlpatterns = [
    path('categories/<cstmslug:category>/article/<slug:slug>/', views.get_article, name='get_article'),
    path('categories/', views.get_all_categories, name='categories'),
    path('categories/<cstmslug:slug>/', views.get_category, name='get_category'),
    path('write/', views.write_article, name='write_article'),
    path('bookmark/', views.bookmark_article, name='bookmark_article'),
    
    
]
