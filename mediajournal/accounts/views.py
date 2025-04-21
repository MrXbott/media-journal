from django.shortcuts import render, redirect
from django.db.models import Count, Q
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.core.exceptions import ValidationError
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404

from .forms import RegistrationForm, ProfileEditForm, UserPhotoForm
from .token import email_verification_token
from .tasks import send_confirm_email
from .models import User, Contact
from articles.models import Article
from news.models import News


def registration(request: HttpRequest) -> HttpResponse:
    """
    Обрабатывает регистрацию нового пользователя.

    Если запрос POST и форма валидна, создаётся пользователь, генерируется токен подтверждения email,
    и отправляется письмо с активационной ссылкой. 
    В противном случае возвращается форма регистрации с ошибками.

    Аргументы:
        request (HttpRequest): HTTP-запрос от клиента.

    Возвращает:
        HttpResponse: Страница с формой регистрации или подтверждением email.
    """
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            current_site = get_current_site(request) 
            subject = settings.CONFIRM_EMAIL_SUBJECT
            message = render_to_string('registration/confirm_email.html', { 
                'user': user, 
                'protocol': 'http:',
                'domain': current_site.domain, 
                'uid': urlsafe_base64_encode(force_bytes(user.id)), 
                'token': email_verification_token.make_token(user), 
            }) 
            to_email = form.cleaned_data.get('email') 
            send_confirm_email.delay(subject, message, to_email)
            return render(request, 'registration/email_confirmation.html', {'user': user})  
        else:
            messages.error(request, 'При создании аккаунта возникла ошибка')
    else:
        form = RegistrationForm()
    return render(request, 'registration/registration.html', {'form': form})


def confirm_email(request: HttpRequest, uidb64: str, token: str) -> HttpResponse:
    """
    Подтверждает email пользователя по уникальной ссылке из письма.

    Декодирует ID пользователя, проверяет токен и активирует аккаунт, если всё валидно.

    Аргументы:
        request (HttpRequest): HTTP-запрос от клиента.
        uidb64 (str): base64-кодированный ID пользователя.
        token (str): Токен подтверждения email.

    Возвращает:
        HttpResponse: Страница об успешной активации или с сообщением об ошибке.
    """
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist): 
        user = None

    if user is not None and email_verification_token.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, 'registration/registration_done.html')
    return render(request, 'registration/activation_error.html')


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    """
    Представление для подтверждения сброса пароля.

    Расширяет стандартный PasswordResetConfirmView, добавляя безопасное извлечение пользователя по uid.
    """
    def get_user(self, uidb64):
        """
        Получает пользователя по закодированному идентификатору.

        Аргументы:
            uidb64 (str): base64-кодированный ID пользователя.

        Возвращает:
            User | None: Пользователь, если найден, иначе None.
        """
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist, ValidationError):
            user = None
        return user


def profile(request, id):
    """
    Отображает публичный профиль пользователя.

    Включает опубликованные статьи и новости, статистику активности и категории.

    Аргументы:
        request (HttpRequest): HTTP-запрос от клиента.
        id (int): ID пользователя.

    Возвращает:
        HttpResponse: Страница профиля пользователя.
    """
    user = get_object_or_404(User, id=id)
    user_articles = user.articles.filter(status=Article.Status.PUBLISHED)\
                                    .select_related('category')\
                                    .annotate(
                                        comments_count=Count('article_comments', filter=Q(article_comments__is_active=True)),
                                        )
    user_news = user.news.filter(status=News.Status.PUBLISHED)\
                            .annotate(comments_count=Count('news_comments', filter=Q(news_comments__is_active=True)))

    counts = {
                'articles_count': len(user_articles),
                'news_count': len(user_news),
                'bookmarks_count': user.bookmarks.count(),
                'followers_count': user.followers.count(),
                'comments_count': user.comments.count(),
                }
    return render(request, 'account/profile.html', {'user': user, 
                                                    'user_articles': user_articles,
                                                    'user_news': user_news,
                                                    'counts': counts,
                                                    })

@login_required
def edit_profile(request):
    """
    Позволяет авторизованному пользователю редактировать свой профиль.

    Загружает и сохраняет форму с данными, если запрос POST, иначе отображает текущие данные.

    Аргументы:
        request (HttpRequest): HTTP-запрос от клиента.

    Возвращает:
        HttpResponse: Страница редактирования профиля.
    """
    if request.method == 'POST':
        form = ProfileEditForm(data=request.POST, files=request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile', request.user.id)
    else:
        form = ProfileEditForm(instance=request.user)
    return render(request, 'account/profile_edit.html', {'form': form})


@login_required
@require_POST
def upload_photo(request):
    """
    Загружает и сохраняет новое фото пользователя (POST-запрос).

    Аргументы:
        request (HttpRequest): HTTP-запрос с файлом изображения.

    Возвращает:
        JsonResponse: Статус выполнения запроса и URL фото или ошибки формы.
    """
    form = UserPhotoForm(request.POST, request.FILES, instance=request.user)
    if form.is_valid():
        form.save()
        return JsonResponse({'status': 'ok', 'photo_url': request.user.photo.url})
    return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)


@login_required
def edit_username(request):
    """
    Позволяет изменить имя пользователя, если оно свободно.

    Проверяет уникальность нового имени и обновляет в базе.

    Аргументы:
        request (HttpRequest): POST-запрос с новым значением username.

    Возвращает:
        JsonResponse: Сообщение об успешном изменении или причине отказа.
    """
    new_username = request.POST.dict()['username']
    user = User.objects.get(id=request.user.id)
    
    if User.objects.filter(username=new_username) and User.objects.filter(username=new_username).first() != user:
        return JsonResponse({'message': 'This username already taken'})
    
    if new_username and new_username != user.username:
        user.username = new_username
        user.save()
        return JsonResponse({'message': 'Your username updated successfully'})
    return JsonResponse({'message': 'You already have this username'})


@require_POST
@login_required
def follow_user(request):
    """
    Обрабатывает подписку/отписку на другого пользователя.

    Принимает ID пользователя и действие ('follow' или 'unfollow') через POST-запрос.

    Аргументы:
        request (HttpRequest): HTTP-запрос с параметрами действия.

    Возвращает:
        JsonResponse: Результат действия и сообщение о статусе.
    """
    user_id = request.POST.get('user_id')
    action = request.POST.get('action')
    if user_id and action:
        try:
            user = User.objects.get(id=user_id)
            if action == 'follow':
                Contact.objects.get_or_create(user_from=request.user, user_to=user)
            else:
                Contact.objects.filter(user_from=request.user, user_to=user).delete()
            return JsonResponse({'status':'ok', 'message': f'successfully {action}ed'})
        except User.DoesNotExist:
            return JsonResponse({'status':'error', 'message': 'user doesn\'t exist'})
    return JsonResponse({'status':'error', 'message': 'wrong id or action'})

