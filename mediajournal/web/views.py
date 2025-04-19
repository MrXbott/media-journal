from django.db.models import Count, F, Value, Q
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib.postgres.search import SearchVector
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from itertools import chain
from operator import attrgetter
import redis

from articles.models import Article, Category, ArticleSection
from news.models import News
from .forms import SearchForm


r = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)

def main_page(request):
    articles = Article.objects.filter(status=Article.Status.PUBLISHED).order_by('-published')
    featured_categories = Category.objects.filter(is_featured=True)
    total_views = {article.id: int(r.get(f'article:{article.id}:views')) if r.get(f'article:{article.id}:views') else 0 for article in articles}
    return render(request, 'index.html', {
        'articles': articles, 
        'featured_categories': featured_categories,
        'total_views': total_views,
        })


@login_required
def user_news_feed(request):
    users = request.user.following.all()
    all_articles = Article.objects.filter(author__in=users, status=Article.Status.PUBLISHED)\
                                .select_related('author', 'category')\
                                .order_by('-published')\
                                .annotate(
                                    bookmarks_count=Count('bookmarked_by'), 
                                    comments_count=Count('article_comments', filter=Q(article_comments__is_active=True))
                                    )
    all_news = News.objects.filter(author__in=users, status=News.Status.PUBLISHED)\
                                .select_related('author')\
                                .order_by('-published')\
                                .annotate(
                                    # bookmarks_count=Count('bookmarked_by'), 
                                    comments_count=Count('news_comments', filter=Q(news_comments__is_active=True))
                                    )
    
    for article in all_articles:
        article.views = int(r.get(f'article:{article.id}:views')) if r.get(f'article:{article.id}:views') else 0

    for n in all_news:
        n.views = int(r.get(f'news:{n.id}:views')) if r.get(f'news:{n.id}:views') else 0

    combined = sorted(chain(all_articles, all_news), key=attrgetter('published'), reverse=True )

    page = request.GET.get('page')
    paginator = Paginator(combined, 3)
    items = []
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)
    
    return render(request, 'user_news_feed.html', {'section': 'user_news_feed',
                                                    'items': items,
                                                    })


def search(request):
    query = None
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            article_search_vector = SearchVector('title', 'text', 'author__username', config='russian')
            article_results = Article.objects.filter(status=Article.Status.PUBLISHED)\
                                            .select_related('category')\
                                            .annotate(search=article_search_vector)\
                                            .filter(search=query).order_by('-published')
            
            section_search_vector = SearchVector('title', 'text', 'quote', config='russian')
            article_ids_from_sections = ArticleSection.objects.filter(article__status=Article.Status.PUBLISHED)\
                                                                .annotate(search=section_search_vector)\
                                                                .filter(search=query)\
                                                                .values_list('article__id', flat=True)
            
            section_results = Article.objects.filter(id__in=set(article_ids_from_sections))\
                                            .select_related('category')\
                                            .annotate(search=article_search_vector)
            
            all_results = article_results.union(section_results)
            
            page = request.GET.get('page')
            paginator = Paginator(all_results.order_by('-published'), 3)
            try:
                results = paginator.page(page)
            except PageNotAnInteger:
                results = paginator.page(1)
            except EmptyPage:
                results = paginator.page(paginator.num_pages)
            return render(request, 'search_results.html', {'query': query, 
                                                          'results': results,
                                                          'results_count': len(all_results)})

    return render(request, 'search_results.html', {})