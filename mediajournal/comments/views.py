from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Comment
from .forms import CommentForm

def comments_list(request):
    page = request.GET.get('page')
    object_id = request.GET.get('id')
    content_type_name = request.GET.get('type')
    try:
        content_object = ContentType.objects.get(model=content_type_name).get_object_for_this_type(id=object_id)
    except:
        return JsonResponse({'status': 'error', 'message': 'article with such id not found'})
    
    if not content_object.enable_comments:
        return JsonResponse({'status': 'error', 'message': 'comments disabled '})
    
    paginator = Paginator(content_object.comments, 2) 
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
    object_id = request.POST.get('object_id')
    content_type_name = request.POST.get('content_type')
    try:
        content_type = ContentType.objects.get(model=content_type_name)
        content_object = content_type.get_object_for_this_type(id=object_id)
    except:
        return JsonResponse({'status': 'error', 'message': 'wrong content type or object id'})

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        if request.method == 'POST':
            form = CommentForm(data=request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                comment = Comment(text=cd['text'], 
                                  author=request.user, 
                                  content_type=content_type, 
                                  object_id=cd['object_id'], 
                                  parent=cd['parent']
                                  )
                comment.save()
                return JsonResponse({'status': 'ok', 
                                     'username': comment.author.username, 
                                     'comment': comment.text, 
                                     'created': comment.created})
            return JsonResponse({'status': 'error', 'message': 'wrong data in the form'})
        elif request.method =='GET':
            parent_id = request.GET.get('parent_id')
            object_id = request.GET.get('object_id')
            content_type_name = request.GET.get('content_type')
            content_type = ContentType.objects.get(model=content_type_name)
            # print('----- ct', content_type)
            data = {'parent': parent_id, 'object_id': object_id, 'content_type': content_type}
            form = CommentForm(data=data)
            return render(request, 'comment_answer_form.html', {'form': form})
