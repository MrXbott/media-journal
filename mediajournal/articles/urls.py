from django.urls import path, register_converter

from . import views
from .converters import CustomSlugConverter

register_converter(CustomSlugConverter, 'cstmslug')

urlpatterns = [
    path('comment/', views.post_comment, name='post_comment'),
    path('<cstmslug:category>/article/<slug:slug>/', views.get_article, name='get_article'),
    path('categories/', views.get_all_categories, name='categories'),
    path('<cstmslug:slug>/', views.get_category, name='get_category'),
    
    
    # path('categories/f"[-a-zA-Z0-9_/]+"/<slug:slug>/', views.get_article, name='get_article'),
]
