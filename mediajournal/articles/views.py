from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
import redis

from .models import Article, Category, Comment, Bookmark
from .forms import CommentForm, ArticleForm, ArticleImageFormSet
from web.models import Image


r = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB, decode_responses=True)

def get_all_categories(request):
    categories = Category.objects.filter(parent=None)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse([{'name' : category.name, 'url': category.get_absolute_url(), 'image': category.image.url} for category in categories[:10]], safe=False)
    return render(request, 'categories.html', {'categories': categories})

def get_category(request, slug):
    category = get_object_or_404(Category, slug=slug[-1])
    articles = (Article.objects.filter(category__in=category.children) | Article.objects.filter(category=category)).distinct()
    total_views = {article.id: int(r.get(f'article:{article.id}:views') if r.get(f'article:{article.id}:views') else 0) for article in articles}
    return render(request, 'category.html', {'category': category, 'articles': articles, 'total_views': total_views})

def get_last_articles(request):
    articles = Article.objects.all().order_by('published')
    default_user_photo = Image.objects.get(type='default_user_photo')
    return render(request, 'last_articles.html', {'articles': articles, 'default_user_photo': default_user_photo})

def get_article(request, category, slug):
    article = get_object_or_404(Article, slug=slug)
    total_views = r.incr(f'article:{article.id}:views')    
    data = {'article': article.id}
    comment_form = CommentForm(data=data)
    print('------ comment form data', comment_form.data)
    return render(request, 'article.html', {'article': article, 'total_views': total_views, 'form': comment_form})


@login_required
def write_article(request):
    if request.method == 'POST':
        form = ArticleForm(data=request.POST, files=request.FILES)
        formset = ArticleImageFormSet(data=request.POST, files=request.FILES)
        if form.is_valid() and formset.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            images = formset.save(commit=False)
            for image in images:
                image.article = article
                image.save()
            return render(request, 'article_send.html')
    else:
        form = ArticleForm()
        formset = ArticleImageFormSet()
        # formset_empty = formset.empty_form
    return render(request, 'article_write.html', {'form': form, 'formset': formset, })
    

@login_required
@require_POST
def post_comment(request):
    form = CommentForm(data=request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        comment = Comment(body=cd['body'], author=request.user, article=cd['article'])
        comment.save()
        return JsonResponse({'status': 'ok', 'username': comment.author.username, 'comment': comment.body, 'created': comment.created})
    return JsonResponse({'status': 'error', 'message': 'wrong data in the form'})


@login_required
@require_POST
def bookmark_article(request):
    article_id = request.POST.get('article_id')
    article = Article.objects.get(id=article_id)
    if article in Article.objects.filter(bookmarked_by=request.user):
        print('article already in bookmarks. deleting')
        Bookmark.objects.filter(user=request.user, article=article).delete()
        return JsonResponse({'bookmark': 'removed'})
    else:
        print('adding article to bookmarks')
        Bookmark.objects.create(user=request.user, article=article)
        return JsonResponse({'bookmark': 'added'})
    
    # return JsonResponse({})