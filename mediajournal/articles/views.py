from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
import redis

from .models import Article, Category, Comment, Bookmark
from .forms import CommentForm, ArticleForm, ArticleImageFormSet, ArticleSectionFormSet
from web.models import Image


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
    # articles = (Article.objects.filter(category__in=category.children) | Article.objects.filter(category=category)).distinct().filter(status=Article.Status.PUBLISHED)
    articles = category.all_children_articles
    total_views = {article.id: int(r.get(f'article:{article.id}:views') if r.get(f'article:{article.id}:views') else 0) for article in articles}
    last_articles = Article.objects.filter(status=Article.Status.PUBLISHED).order_by('-published')[:5]
    return render(request, 'category.html', {'category': category, 
                                             'articles': articles, 
                                             'total_views': total_views,
                                             'last_articles': last_articles,
                                             })

def get_last_articles(request):
    articles = Article.objects.all().order_by('published')
    default_user_photo = Image.objects.get(type='default_user_photo')
    return render(request, 'last_articles.html', {'articles': articles, 'default_user_photo': default_user_photo})

def get_article(request, category, slug):
    # print('body: ', request.body)
    # print('path: ', request.path)
    # print('resolver_match: ', request.resolver_match)
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
        print('---- sections: ', section_formset)
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
    

def comments_list(request):
    page = request.GET.get('page')
    article_id = request.GET.get('article_id')
    try:
        article = Article.objects.get(id=article_id)
    except:
        return JsonResponse({'status': 'error', 'message': 'article with such id not found'})
    if not article.enable_comments:
        return JsonResponse({'status': 'error', 'message': 'comments disabled '})
    
    comments = Comment.objects.filter(is_active=True, article__id=article_id, parent=None) 
    paginator = Paginator(comments, 2) 
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return HttpResponse('')
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'comments_list.html', {'comments': comments})

@login_required
def post_comment(request):
    print('----rm', request.method)
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        if request.method == 'POST':
            print(request.POST)
            form = CommentForm(data=request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                comment = Comment(body=cd['body'], author=request.user, article=cd['article'], parent=cd['parent'])
                comment.save()
                return JsonResponse({'status': 'ok', 'username': comment.author.username, 'comment': comment.body, 'created': comment.created})
            return JsonResponse({'status': 'error', 'message': 'wrong data in the form'})
        elif request.method =='GET':
            print(request.GET)
            parent_id = request.GET.get('parent_id')
            article_id = request.GET.get('article_id')
            data = {'parent': parent_id, 'article': article_id}
            form = CommentForm(data=data)
            return render(request, 'comment_answer_form.html', {'form': form})
        

# @login_required
# def answer_comment(request):
#     print('----rm', request.method)
#     if request.headers.get('x-requested-with') == 'XMLHttpRequest':
#         if request.method == 'POST':
#             form = CommentForm(data=request.POST)
#             if form.is_valid():
#                 cd = form.cleaned_data
#                 print('----- cd ', cd)
#                 return JsonResponse({})
#         elif request.method =='GET':
#             # data = {'article': article.id}
#             form = CommentForm()
#             return render(request, 'comment_answer_form.html', {'form': form})


@login_required
@require_POST
def bookmark_article(request):
    article_id = request.POST.get('article_id')
    # to do: add safe get
    article = Article.objects.get(id=article_id)
    if article in Article.objects.filter(bookmarked_by=request.user):
        print('article already in bookmarks. deleting')
        Bookmark.objects.filter(user=request.user, article=article).delete()
        return JsonResponse({'bookmark': 'removed'})
    else:
        print('adding article to bookmarks')
        Bookmark.objects.create(user=request.user, article=article)
        return JsonResponse({'bookmark': 'added'})
    
