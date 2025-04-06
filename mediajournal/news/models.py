from django.db import models
from django.urls import reverse
from django.contrib.contenttypes.fields import GenericRelation
from datetime import datetime


class News(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'Draft'
        PUBLISHED = 'Published'
        REJECTED = 'Rejected'

    title = models.CharField(max_length=300, blank=False, null=False, unique=False)
    text = models.TextField()
    author = models.ForeignKey('accounts.User', null=True, on_delete=models.SET_NULL, related_name='news')
    published = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
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
            self.published = datetime.now()
        super(News, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('one_news', kwargs={'news_id': self.id})
    