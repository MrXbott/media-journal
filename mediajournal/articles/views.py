from django.shortcuts import render
from django.conf import settings
import redis

from .models import Article, Category
from web.models import Image


r = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB, decode_responses=True)

def get_all_categories(request):
    categories = Category.objects.filter(parent=None)
    return render(request, 'categories.html', {'categories': categories})

def get_category(request, slug):
    category = Category.objects.get(slug=slug[-1])
    articles = (Article.objects.filter(category__in=category.children) | Article.objects.filter(category=category)).distinct()
    total_views = {article.id: int(r.get(f'article:{article.id}:views')) for article in articles}
    return render(request, 'category.html', {'category': category, 'articles': articles, 'total_views': total_views})

def get_last_articles(request):
    articles = Article.objects.all().order_by('published')
    default_user_photo = Image.objects.get(type='default_user_photo')
    return render(request, 'last_articles.html', {'articles': articles, 'default_user_photo': default_user_photo})

def get_article(request, category, slug):
    article = Article.objects.get(slug=slug)
    total_views = r.incr(f'article:{article.id}:views')
    print('---------', article.category.parents)
    
    return render(request, 'article.html', {'article': article, 'total_views': total_views})
