from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
import redis

from .models import Article, Category

from .forms import ArticleForm, ArticleImageFormSet, ArticleSectionFormSet
from comments.forms import CommentForm


r = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB, decode_responses=True)

def get_all_categories(request):
    """
    Отображает все основные категории (не имеющие родителя).

    Аргументы:
        request (HttpRequest): HTTP-запрос от клиента.

    Возвращает:
        HttpResponse: HTTP-ответ с шаблоном для отображения всех категорий.
    """
    categories = Category.objects.filter(parent=None)
    return render(request, 'categories.html', {'categories': categories, 
                                               'section': 'categories'
                                               })

def get_category(request, slug):
    """
    Отображает статьи в конкретной категории.

    Загружает все статьи из этой категории и из ее дочерних категорий, 
    выполняет пагинацию и отображает статьи на странице.

    Аргументы:
        request (HttpRequest): HTTP-запрос от клиента.
        slug (str): Слаг категории для поиска.

    Возвращает:
        HttpResponse: HTTP-ответ с шаблоном для отображения статей в выбранной категории.
    """
    category = get_object_or_404(Category, slug=slug[-1])
    all_articles = category.all_children_articles
    page = request.GET.get('page')
    paginator = Paginator(all_articles, 3)

    articles = []
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)

    for article in articles:
        article.is_bookmarked = article.bookmarks.filter(user=request.user).exists()
    total_views = {article.id: int(r.get(f'article:{article.id}:views') if r.get(f'article:{article.id}:views') else 0) for article in articles}
    return render(request, 'category.html', {'category': category, 
                                             'articles': articles, 
                                             'page': page,
                                             'total_views': total_views,
                                             })


def get_article(request, category, slug):
    """
    Загружает статью по её слагу, увеличивает количество просмотров в Redis и отображает её на странице.

    Аргументы:
        request (HttpRequest): HTTP-запрос от клиента.
        category (str): Категория статьи (не используется напрямую, нужна при парсинге слага).
        slug (str): Слаг статьи для поиска.

    Возвращает:
        HttpResponse: HTTP-ответ с шаблоном для отображения статьи.
    """
    article = get_object_or_404(Article, slug=slug)
    total_views = r.incr(f'article:{article.id}:views')    
    data = {'article': article.id, 'parent': ''}
    comment_form = CommentForm(data=data)
    article.is_bookmarked = article.bookmarks.filter(user=request.user).exists()
    return render(request, 'article.html', {'article': article, 
                                            'total_views': total_views, 
                                            'form': comment_form, 
                                            })


@login_required
def write_article(request):
    """
    Позволяет пользователю создать и сохранить новую статью.

    Если запрос POST и все формы валидны, сохраняет статью, её изображения и разделы в базе. 
    В противном случае отображает формы для ввода данных.

    Аргументы:
        request (HttpRequest): HTTP-запрос от клиента.

    Возвращает:
        HttpResponse: HTTP-ответ с шаблоном для создания статьи или подтверждения отправки.
    """
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
        

    
