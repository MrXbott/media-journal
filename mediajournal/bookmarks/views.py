from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse, HttpResponse
from django.contrib.contenttypes.models import ContentType

from .models import Bookmark
from articles.models import Article
from news.models import News


@login_required
@require_POST
def add_remove_bookmark(request):
    # article_id = request.POST.get('article_id')
    object_id = request.POST.get('object_id')
    content_type_name = request.POST.get('content_type')
    try:
        content_type = ContentType.objects.get(model=content_type_name)
        content_object = content_type.get_object_for_this_type(id=object_id)
    except:
        return JsonResponse({'status': 'error', 'message': 'wrong content type or object id'})
    # user_bookmarks = Bookmark.objects.filter(user=request.user).values_list('content_object', flat=True)
    print('------', content_type, content_object)
    print(request.user)
    print(request.user.bookmarks.all())
    # try:
    #     article = Article.objects.get(id=article_id)
    # except Article.DoesNotExist:
    #     return JsonResponse({'status': 'error', 'message': 'article doesn\'t exist'})
    
    if Bookmark.objects.filter(user=request.user, object_id=object_id, content_type=content_type).exists():
        Bookmark.objects.filter(user=request.user, content_type=content_type, object_id=object_id).delete()
        return JsonResponse({'status': 'ok', 'bookmark': 'removed'})
    else:
        Bookmark.objects.create(user=request.user, content_type=content_type, object_id=object_id)
        return JsonResponse({'status': 'ok', 'bookmark': 'added'})

    # return JsonResponse()