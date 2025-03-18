from django.db import models
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.core.exceptions import ValidationError
from datetime import datetime

from accounts.models import User
from .ru_slugify import slugify

class SafeGetManager(models.Manager):
    def safe_get(self, **kwargs):
        try:
            return self.get(**kwargs)
        except self.model.DoesNotExist:
            return None
        # except self.model.MultipleObjectsReturned:
        #     return None

class Article(models.Model):
    objects = SafeGetManager()

    class Status(models.TextChoices):
        MODERATION = 'Moderation'
        REJECTED = 'Rejected'
        PUBLISHED = 'Published'

    title = models.CharField(max_length=300, blank=False, null=False, unique=False)
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='articles')
    body = models.TextField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.MODERATION)
    created = models.DateTimeField(auto_now_add=True)
    published = models.DateTimeField(blank=True, null=True)
    slug = models.SlugField(max_length=250, unique_for_date='published', blank=True, null=True, unique=True)
    category = models.ForeignKey('Category', blank=False, null=True, on_delete=models.SET_NULL)
    cover_image = models.ImageField(upload_to='images/', blank=True, null=True, default='default/default_article_cover.jpg')
    bookmarked_by = models.ManyToManyField(User, through='Bookmark')
    enable_comments = models.BooleanField(default=True)

    class Meta:
        ordering = ['published']

    @property
    def comments(self):
        return self.article_comments.filter(is_active=True)

    def __str__(self) -> str:
        return self.title
    
    def get_absolute_url(self):
        return reverse('get_article', kwargs={'slug': self.slug, 'category': self.category.full_slug})
    
    def preview(self):
        return mark_safe(f'<img src="{self.cover_image.url}" width="100"/>')
    
    def save(self, *args, **kwargs):
        if self.status == self.Status.PUBLISHED and not self.published:
            self.published = datetime.now()
        super(Article, self).save(*args, **kwargs)

    def clean(self):
        if self.status == self.Status.PUBLISHED and not self.slug:
            raise ValidationError({'slug': 'Enter a slug because you want to publish the article'})
    

class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookmarks')
    article = models.ForeignKey(Article, on_delete=models.CASCADE)

    class Meta:
        constraints = [
        models.UniqueConstraint(
            fields=['user_id', 'article_id'], 
            name='unique bookmark')
    ]

class Category(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False, unique=True)
    parent = models.ForeignKey('Category', blank=True, null=True, unique=False, related_name='subcategories', on_delete=models.SET_NULL)
    slug = models.SlugField(max_length=250, blank=True, null=False, unique=True)
    image = models.ImageField(upload_to='category-images/', blank=True, null=True, unique=False)

    class Meta:
        ordering = ['name']

    @property
    def full_slug(self):
        return self._get_parent_slugs()
    
    @property
    def children(self):
        return Category.objects.filter(parent=self)
    
    @property
    def parents(self):
        if self.parent:
            parents = self.parent.parents + [self.parent]
            return parents
        else:
            return []

    def __str__(self) -> str:
        if self.parent:
            return f'{self.parent} > {self.name}'
        return self.name
    
    def _get_parent_slugs(self):
        if not self.parent:
            return self.slug
        else:
            return f'{self.parent._get_parent_slugs()}/{self.slug}'
    
    def get_absolute_url(self):
        return reverse("get_category", kwargs={'slug': self.full_slug})
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

class Comment(models.Model):
    author = models.ForeignKey(User, related_name='comments', null=True, on_delete=models.SET_NULL)
    article = models.ForeignKey(Article, related_name='article_comments', on_delete=models.CASCADE)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('Comment', blank=True, null=True, unique=False, on_delete=models.SET_NULL, related_name='answers')
    is_active = models.BooleanField(default=False)

    class Meta:
        ordering = ['created']

    @property
    def children(self):
        return Comment.objects.filter(parent=self, is_active=True, article=self.article)

    def __str__(self) -> str:
        return f'Comment by {self.author.username if self.author else "User deleted"} on {self.article.title}'
    
class ArticleImage(models.Model):
    image = models.ImageField(upload_to='images/', blank=False, null=False)
    article = models.ForeignKey(Article, related_name='images', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.image.name
    
    def preview(self):
        return mark_safe(f'<img src="{self.image.url}" width="100"/>')