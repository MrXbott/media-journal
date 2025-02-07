from django.shortcuts import render
from django.conf import settings
import redis

from articles.models import Article, Category
from web.models import Image

r = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)

def main_page(request):
    articles = Article.objects.all().order_by('published')
    categories = Category.objects.filter(parent=None)
    default_user_photo = Image.objects.get(type='default_user_photo')
    total_views = {article.id: int(r.get(f'article:{article.id}:views')) for article in articles}
    
    return render(request, 'main.html', {
        'articles': articles, 
        'categories': categories,
        'default_user_photo': default_user_photo, 
        'total_views': total_views
        })
