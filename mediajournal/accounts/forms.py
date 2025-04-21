from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password, password_validators_help_text_html
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.forms import AuthenticationForm
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template import loader
from typing import Any, Dict

from .models import User
from .tasks import send_password_reset_email

class RegistrationForm(forms.ModelForm):
    """
    Форма для регистрации нового пользователя. Включает поля email, пароль и повтор пароля.

    Атрибуты:
        password1 (CharField): Поле для ввода пароля.
        password2 (CharField): Поле для подтверждения пароля.

    Методы:
        clean_password2: Проверяет совпадение двух введённых паролей.
        save: Сохраняет пользователя с хешированным паролем.
    """
    error_css_class = 'error'
    required_css_class = 'required'

    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput, validators=[validate_password], help_text=password_validators_help_text_html)
    password2 = forms.CharField(label='Пароль еще раз', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email']

    def clean_password2(self):
        """
        Проверяет, совпадают ли введённые пароли (password1 и password2).
        
        Raises:
            ValidationError: Если пароли не совпадают.

        Returns:
            str: Подтверждённый пароль.
        """
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError('Пароли не совпадают')
        return password2
    
    def save(self, commit=True):
        """
        Сохраняет пользователя с хешированным паролем.

        Аргументы:
            commit (bool): Если True, объект будет сохранён в базе.

        Returns:
            User: Созданный пользователь.
        """
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user
    

class CustomPasswordResetForm(forms.Form):
    """
    Кастомная форма для сброса пароля. Отправляет email с ссылкой на восстановление через Celery-задачу.

    Атрибуты:
        email (EmailField): Email пользователя для отправки ссылки сброса пароля.

    Методы:
        get_user: Возвращает активного пользователя с данным email.
        save: Генерирует ссылку для сброса пароля и отправляет email.
        send_mail: Формирует письмо и отправляет его через фоновую задачу Celery.
    """

    email = forms.EmailField(label='Эл. адрес', max_length=254, widget=forms.EmailInput(attrs={"autocomplete": "email"}),)

    def get_user(self, email):
        """
        Получает активного пользователя по email.

        Аргументы:
            email (str): Email пользователя.

        Returns:
            User | None: Объект пользователя или None, если не найден.
        """
        try:
            user = User.objects.get(email=email, is_active=True)
        except User.DoesNotExist:
            user = None
        return user
    
    def save(
        self,
        domain_override=None,
        subject_template_name="registration/password_reset_subject.txt",
        email_template_name="registration/password_reset_email.html",
        use_https=False,
        token_generator=default_token_generator,
        from_email=None,
        request=None,
        html_email_template_name=None,
        extra_email_context=None,
    ):
        """
        Генерирует одноразовую ссылку для сброса пароля и отправляет её пользователю.

        Аргументы:
            domain_override (str, optional): Явное указание домена.
            subject_template_name (str): Шаблон темы письма.
            email_template_name (str): Шаблон тела письма.
            use_https (bool): Использовать HTTPS в ссылке.
            token_generator (TokenGenerator): Генератор токенов.
            from_email (str): Адрес отправителя.
            request (HttpRequest): Текущий запрос.
            html_email_template_name (str, optional): HTML-шаблон письма.
            extra_email_context (dict, optional): Дополнительный контекст.
        """
        email = self.cleaned_data["email"]
        if not domain_override:
            current_site = get_current_site(request)
            site_name = current_site.name
            domain = current_site.domain
        else:
            site_name = domain = domain_override

        user = self.get_user(email)
        context = {
            "email": user.email,
            "domain": domain,
            "site_name": site_name,
            "uid": urlsafe_base64_encode(force_bytes(user.id)),
            "user": user,
            "token": token_generator.make_token(user),
            "protocol": "https" if use_https else "http",
        }
        self.send_mail(subject_template_name, email_template_name, context, from_email, email)
    
    def send_mail(self, subject_template_name: str, email_template_name: str, context: Dict[str, Any], from_email: str | None, to_email: str, html_email_template_name: str | None = ...) -> None:
        """
        Формирует и отправляет email со ссылкой на сброс пароля через Celery-задачу.

        Аргументы:
            subject_template_name (str): Шаблон темы письма.
            email_template_name (str): Шаблон тела письма.
            context (dict): Контекст для шаблонов.
            from_email (str | None): Email отправителя.
            to_email (str): Email получателя.
            html_email_template_name (str | None): HTML-шаблон письма.
        """
        subject = loader.render_to_string(subject_template_name, context)
        subject = "".join(subject.splitlines())
        body = loader.render_to_string(email_template_name, context)

        send_password_reset_email.delay(subject, body, from_email, to_email)


# class CustomAuthenticationForm(AuthenticationForm):
#     def __init__(self, *args, **kwargs):
#         super(CustomAuthenticationForm, self).__init__(*args, **kwargs)
#         self.fields['username'].widget.attrs['placeholder'] = 'Email'
#         self.fields['username'].widget.attrs['class'] = 'form-control'
#         self.fields['password'].widget.attrs['placeholder'] = 'Password'
#         self.fields['password'].widget.attrs['class'] = 'form-control'


class UserPhotoForm(forms.ModelForm):
    """
    Форма для загрузки фото пользователя.

    Проверяет:
        - Размер не больше 1MB.
        - Поддерживаемые типы: JPEG, PNG, GIF.
    """
    class Meta:
        model = User
        fields = ['photo']

    def clean_photo(self):
        """
        Проверяет размер и формат изображения.

        Исключения:
            ValidationError: Если изображение больше 1MB или неподдерживаемого формата.

        Возвращает:
            File: Загруженное изображение.
        """
        photo = self.cleaned_data['photo']
        if photo:
            if photo.size > 1024 * 1024:  # 1MB
                raise forms.ValidationError('Размер файла должен быть не больше 1MB.')
            if not photo.content_type in ['image/jpeg', 'image/png', 'image/gif']:
                raise forms.ValidationError('Допустимы только файлы JPEG или PNG.')
        return photo

class ProfileEditForm(forms.ModelForm):
    """
    Форма для редактирования профиля пользователя (кроме email - его редактировать запрещено).

    Атрибуты:
        username (CharField): Имя пользователя.
        email (EmailField): Только для отображения, нельзя редактировать.
        designation (CharField): Девиз или статус.
        bio (TextField): Биография пользователя.

    В init задаются placeholder'ы и отключается редактирование email.
    """
    class Meta:
        model = User
        fields = ['username', 'email', 'designation', 'bio']
        widgets = {
            'photo': forms.FileInput(),
        }

    def __init__(self, *args, **kwargs):
        """
        Устанавливает плейсхолдеры для полей и делает email недоступным для редактирования.
        """
        super().__init__(*args, **kwargs)
        self.fields['email'].disabled = True
        self.fields['designation'].widget.attrs['placeholder'] = 'Ваш девиз или любимая цитата...'
        self.fields['bio'].widget.attrs['placeholder'] = 'Напишите что-нибудь о себе...'
