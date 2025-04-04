from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser
from django.core.validators import RegexValidator
from django.utils import timezone
from django.urls import reverse

from articles.models import Article
from news.models import News

class Staff(AbstractUser):
    email = models.EmailField(blank=False, unique=True, null=False, verbose_name='Эл. адрес')

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'

    def __str__(self):
        return f'{self.email} ({self.first_name} {self.last_name})'


class User(AbstractBaseUser):
    username = models.CharField(max_length=100, blank=True, null=True, unique=True, verbose_name='Имя пользователя')
    email = models.EmailField(blank=False, unique=True, null=False, verbose_name='Эл. адрес')
    phone_validator = RegexValidator(regex=r'^[+][7][(]\d{3}[)]\d{3}-\d{2}-\d{2}$', message="Введите номер телефона в формате: '+7(999)999-99-99'. ")
    phone = models.CharField(max_length=18, validators=[phone_validator], blank=True, unique=True, null=True, verbose_name='Моб. тел.')
    password = models.CharField(max_length=128, blank=False, unique=False, null=False, verbose_name='Пароль')
    date_joined = models.DateTimeField(default=timezone.now, verbose_name='Дата регистрации')
    is_active = models.BooleanField(default=False)
    photo = models.ImageField(upload_to='photo/', blank=True, null=True, default='default/default_user_photo.jpg')
    designation = models.CharField(max_length=150, blank=True, null=True, unique=False)
    bio = models.TextField(max_length=1000, blank=True, null=True, unique=False)

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def published_articles(self):
        return self.articles.filter(status=Article.Status.PUBLISHED)
    
    @property
    def published_news(self):
        return self.news.filter(status=News.Status.PUBLISHED)

    def __str__(self):
        return self.email
    
    def save(self, *args, **kwargs):
        if not self.email and not self.phone:
            raise Exception('User must have an email or a phone or both')
        super(User, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("profile", kwargs={"id": self.id})
    
    
    