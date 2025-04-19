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
    '''A form for creating new users. Includes all the required
    fields, plus a repeated password.
    '''
    error_css_class = 'error'
    required_css_class = 'required'

    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput, validators=[validate_password], help_text=password_validators_help_text_html)
    password2 = forms.CharField(label='Пароль еще раз', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email']

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError('Пароли не совпадают')
        return password2
    
    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user
    

class CustomPasswordResetForm(forms.Form):
    '''Сustom form to send email in a celery background task.'''

    email = forms.EmailField(label='Эл. адрес', max_length=254, widget=forms.EmailInput(attrs={"autocomplete": "email"}),)

    def get_user(self, email):
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
        Generate a one-use only link for resetting password and send it to the
        user.
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
        subject = loader.render_to_string(subject_template_name, context)
        # Email subject *must not* contain newlines
        subject = "".join(subject.splitlines())
        body = loader.render_to_string(email_template_name, context)

        send_password_reset_email.delay(subject, body, from_email, [to_email])


# class CustomAuthenticationForm(AuthenticationForm):
#     def __init__(self, *args, **kwargs):
#         super(CustomAuthenticationForm, self).__init__(*args, **kwargs)
#         self.fields['username'].widget.attrs['placeholder'] = 'Email'
#         self.fields['username'].widget.attrs['class'] = 'form-control'
#         self.fields['password'].widget.attrs['placeholder'] = 'Password'
#         self.fields['password'].widget.attrs['class'] = 'form-control'


class UserPhotoForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['photo']

    def clean_photo(self):
        photo = self.cleaned_data['photo']
        if photo:
            if photo.size > 1024 * 1024:  # 1MB
                raise forms.ValidationError('Размер файла должен быть не больше 1MB.')
            if not photo.content_type in ['image/jpeg', 'image/png', 'image/gif']:
                raise forms.ValidationError('Допустимы только файлы JPEG или PNG.')
        return photo

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'designation', 'bio']
        widgets = {
            'photo': forms.FileInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].disabled = True
        self.fields['designation'].widget.attrs['placeholder'] = 'Ваш девиз или любимая цитата...'
        self.fields['bio'].widget.attrs['placeholder'] = 'Напишите что-нибудь о себе...'
