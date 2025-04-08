from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
import redis

from .models import Article, Category, Bookmark

from .forms import ArticleForm, ArticleImageFormSet, ArticleSectionFormSet
from comments.forms import CommentForm


r = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB, decode_responses=True)

def get_all_categories(request):
    categories = Category.objects.filter(parent=None)
    last_articles = Article.objects.filter(status=Article.Status.PUBLISHED).order_by('-published')[:5]
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse([{'name' : category.name, 'url': category.get_absolute_url(), 'image': category.image.url} for category in categories[:10]], safe=False)
    return render(request, 'categories.html', {'categories': categories, 
                                               'last_articles': last_articles,
                                               'section': 'categories'
                                               })

def get_category(request, slug):
    category = get_object_or_404(Category, slug=slug[-1])
    all_articles = category.all_children_articles
    page = request.GET.get('page')
    paginator = Paginator(all_articles, 3)

    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)

    categories = Category.objects.filter(parent=None).order_by('name')
    total_views = {article.id: int(r.get(f'article:{article.id}:views') if r.get(f'article:{article.id}:views') else 0) for article in articles}
    last_articles = Article.objects.filter(status=Article.Status.PUBLISHED).order_by('-published')[:5]
    return render(request, 'category.html', {'category': category, 
                                             'articles': articles, 
                                             'page': page,
                                             'total_views': total_views,
                                             'last_articles': last_articles,
                                             'categories': categories,
                                             })

def get_last_articles(request):
    articles = Article.objects.all().order_by('published')
    return render(request, 'last_articles.html', {'articles': articles, })

def get_article(request, category, slug):
    article = get_object_or_404(Article, slug=slug)
    total_views = r.incr(f'article:{article.id}:views')    
    data = {'article': article.id, 'parent': ''}
    comment_form = CommentForm(data=data)
    categories = Category.objects.filter(parent=None).order_by('name')
    last_articles = Article.objects.filter(status=Article.Status.PUBLISHED).order_by('-published')[:5]
    return render(request, 'article.html', {'article': article, 
                                            'total_views': total_views, 
                                            'form': comment_form, 
                                            'categories': categories,
                                            'last_articles': last_articles,
                                            })


@login_required
def write_article(request):
    if request.method == 'POST':
        article_form = ArticleForm(data=request.POST, files=request.FILES)
        image_formset = ArticleImageFormSet(data=request.POST, files=request.FILES, prefix='images')
        section_formset = ArticleSectionFormSet(data=request.POST, prefix='sections')
        if article_form.is_valid() and image_formset.is_valid() and section_formset.is_valid():
            article = article_form.save(commit=False)
            article.author = request.user
            article.save()
            images = image_formset.save(commit=False)
            for image in images:
                image.article = article
                image.save()
            sections = section_formset.save(commit=False)
            
            for section in sections:
                section.article = article
                section.save()
            return render(request, 'article_sent.html')
        else:
            pass 
    else:
        article_form = ArticleForm()
        section_formset = ArticleSectionFormSet(prefix='sections')
        image_formset = ArticleImageFormSet(prefix='images')
    return render(request, 'article_write.html', {'article_form': article_form, 
                                                  'section_formset': section_formset, 
                                                  'image_formset': image_formset, 
                                                  'section': 'write',
                                                  })
        

@login_required
@require_POST
def bookmark_article(request):
    article_id = request.POST.get('article_id')
    try:
        article = Article.objects.get(id=article_id)
    except Article.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'article doesn\'t exist'})
    
    if article in Article.objects.filter(bookmarked_by=request.user):
        Bookmark.objects.filter(user=request.user, article=article).delete()
        return JsonResponse({'status': 'ok', 'bookmark': 'removed'})
    else:
        Bookmark.objects.create(user=request.user, article=article)
        return JsonResponse({'status': 'ok', 'bookmark': 'added'})
    
    
