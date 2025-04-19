from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericRelation
from django.utils.safestring import mark_safe


class News(models.Model):
    """
    Модель новостной записи, предназначенная для публикации коротких информационных сообщений.
    """
    class Status(models.TextChoices):
        MODERATION = 'Moderation'
        PUBLISHED = 'Published'
        REJECTED = 'Rejected'

    title = models.CharField(max_length=300, blank=False, null=False, unique=False)
    text = models.TextField()
    author = models.ForeignKey('accounts.User', null=True, on_delete=models.SET_NULL, related_name='news')
    published = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.MODERATION)
    cover = models.ImageField(upload_to='images/', blank=True, null=True, default='default/default_news_cover.jpg')
    enable_comments = models.BooleanField(default=True)
    news_comments = GenericRelation('comments.Comment')

    class Meta:
        ordering = ['-published']

    @property
    def comments(self):
        return self.news_comments.filter(is_active=True)

    def __str__(self) -> str:
        return self.title
    
    def save(self, *args, **kwargs):
        if self.status == self.Status.PUBLISHED and not self.published:
            self.published = timezone.now()
        super(News, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('one_news', kwargs={'news_id': self.id})
    
    def cover_preview(self):
        return mark_safe(f'<img src="{self.cover.url}" width="100"/>')
    