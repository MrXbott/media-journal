from django.shortcuts import render, get_object_or_404
import redis
from django.conf import settings

from .models import News
from .forms import SuggestNewsForm
from articles.models import Category, Article


r = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB, decode_responses=True)

def get_all_news(request):
    news = News.objects.filter(status=News.Status.PUBLISHED).order_by('-published')
    categories = Category.objects.filter(parent=None)
    last_articles = Article.objects.filter(status=Article.Status.PUBLISHED).order_by('-published')[:5]
    total_views = {n.id: int(r.get(f'news:{n.id}:views') if r.get(f'news:{n.id}:views') else 0) for n in news}
    return render(request, 'all_news.html', {'news': news, 
                                             'section': 'news',
                                             'categories': categories,
                                             'last_articles': last_articles,
                                             'total_views': total_views,
                                             })

def get_one_news(request, news_id):
    one_news = get_object_or_404(News, id=news_id)
    categories = Category.objects.filter(parent=None)
    last_articles = Article.objects.filter(status=Article.Status.PUBLISHED).order_by('-published')[:5]
    total_views = r.incr(f'news:{news_id}:views')    
    return render(request, 'one_news.html', {'one_news': one_news, 
                                             'section': 'news',
                                             'categories': categories,
                                             'last_articles': last_articles,
                                             'total_views': total_views,
                                             })


def suggest_news(request):
    if request.method == 'POST':
        form = SuggestNewsForm(data=request.POST)
        if form.is_valid():
            news = form.save(commit=False)
            news.author = request.user
            news.save()
            return render(request, 'news_sent.html')
    else:
        form = SuggestNewsForm()
        return render(request, 'suggest_news.html', {'form': form, 
                                                 'section': 'suggest_news'
                                                 })