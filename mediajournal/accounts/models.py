from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser
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
    username = models.CharField(max_length=100, blank=False, null=False, unique=True, verbose_name='Имя пользователя')
    email = models.EmailField(blank=False, unique=True, null=False, verbose_name='Эл. адрес')
    password = models.CharField(max_length=128, blank=False, unique=False, null=False, verbose_name='Пароль')
    date_joined = models.DateTimeField(default=timezone.now, verbose_name='Дата регистрации')
    is_active = models.BooleanField(default=False)
    photo = models.ImageField(upload_to='photo/', blank=True, null=True, default='default/default_user_photo.jpg')
    designation = models.CharField(max_length=150, blank=True, null=True, unique=False)
    bio = models.TextField(max_length=1000, blank=True, null=True, unique=False)
    following = models.ManyToManyField('self', through='Contact', related_name='followers', symmetrical=False)

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email']

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
        if not self.username:
            self.username = self.email
        super(User, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('profile', kwargs={'id': self.id})
    
    
class Contact(models.Model):
    user_from = models.ForeignKey(User, related_name='rel_from_set', on_delete=models.CASCADE)
    user_to = models.ForeignKey(User, related_name='rel_to_set', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created'])
        ]

    def __str__(self):
        return f'{self.user_from} follows {self.user_to}'