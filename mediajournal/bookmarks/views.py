from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.contrib.contenttypes.models import ContentType

from .models import Bookmark


@login_required
@require_POST
def add_remove_bookmark(request):
    """
    Обработчик для добавления или удаления закладки для объекта.

    Этот метод проверяет, существует ли закладка для указанного объекта у текущего пользователя. 
    Если закладка существует, она удаляется. 
    Если закладки нет, то создается новая закладка.

    Аргументы:
        request (HttpRequest): Объект запроса, содержащий данные POST с идентификатором объекта и типом контента.

    Возвращает:
        JsonResponse: Ответ в формате JSON, содержащий статус операции (успех или ошибка) и информацию о том, 
        была ли добавлена или удалена закладка.
    """
    object_id = request.POST.get('object_id')
    content_type_name = request.POST.get('content_type')
    try:
        content_type = ContentType.objects.get(model=content_type_name)
        content_object = content_type.get_object_for_this_type(id=object_id)
    except:
        return JsonResponse({'status': 'error', 'message': 'wrong content type or object id'})
    
    if Bookmark.objects.filter(user=request.user, object_id=object_id, content_type=content_type).exists():
        Bookmark.objects.filter(user=request.user, content_type=content_type, object_id=object_id).delete()
        return JsonResponse({'status': 'ok', 'bookmark': 'removed'})
    else:
        Bookmark.objects.create(user=request.user, content_type=content_type, object_id=object_id)
        return JsonResponse({'status': 'ok', 'bookmark': 'added'})
