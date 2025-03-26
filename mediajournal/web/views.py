from django.shortcuts import render
from django.conf import settings
import redis

from articles.models import Article, Category
from web.models import Image

r = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)

def main_page(request):
    articles = Article.objects.filter(status=Article.Status.PUBLISHED).order_by('-published')
    featured_categories = Category.objects.filter(is_featured=True)

    total_views = {article.id: int(r.get(f'article:{article.id}:views')) if r.get(f'article:{article.id}:views') else 0 for article in articles}
    
    return render(request, 'index.html', {
        'articles': articles, 
        'featured_categories': featured_categories,
        'total_views': total_views
        })
