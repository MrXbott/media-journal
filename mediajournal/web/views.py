from django.shortcuts import render
from django.conf import settings
import redis

from articles.models import Article, Category
from web.models import Image

r = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)

def main_page(request):
    articles = Article.objects.filter(status=Article.Status.PUBLISHED).order_by('-published')
    default_user_photo = Image.objects.get(type='default_user_photo')
    total_views = {article.id: int(r.get(f'article:{article.id}:views')) if r.get(f'article:{article.id}:views') else 0 for article in articles}
    
    return render(request, 'main.html', {
        'articles': articles, 
        'default_user_photo': default_user_photo, 
        'total_views': total_views
        })
