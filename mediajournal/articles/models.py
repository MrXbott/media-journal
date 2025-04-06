from django.db import models
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.core.exceptions import ValidationError
from django.contrib.contenttypes.fields import GenericRelation
from datetime import datetime

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
    author = models.ForeignKey('accounts.User', null=True, on_delete=models.SET_NULL, related_name='articles')
    text = models.TextField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.MODERATION)
    created = models.DateTimeField(auto_now_add=True)
    published = models.DateTimeField(blank=True, null=True)
    slug = models.SlugField(max_length=250, unique_for_date='published', blank=True, null=True, unique=True)
    category = models.ForeignKey('Category', blank=False, null=True, on_delete=models.SET_NULL, related_name='articles')
    cover_image = models.ImageField(upload_to='images/', blank=True, null=True, default='default/default_article_cover.jpg')
    bookmarked_by = models.ManyToManyField('accounts.User', through='Bookmark')
    enable_comments = models.BooleanField(default=True)
    article_comments = GenericRelation('comments.Comment')

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
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='bookmarks')
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
    is_featured = models.BooleanField(default=False)

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
        
    @property
    def all_children_articles(self):
        return self._get_children_articles()

    def __str__(self) -> str:
        if self.parent:
            return f'{self.parent} > {self.name}'
        return self.name
    
    def _get_parent_slugs(self):
        if not self.parent:
            return self.slug
        else:
            return f'{self.parent._get_parent_slugs()}/{self.slug}'
        
    def _get_children_articles(self):
        self_articles = self.articles.filter(status=Article.Status.PUBLISHED)
        if self.children:
            articles = Article.objects.none()
            for child in self.children:
                child_articles = child._get_children_articles()
                articles = articles.union(child_articles) 
            return articles.union(self_articles).order_by('-published')
        else:
            return self_articles.order_by('-published')
    
    def get_absolute_url(self):
        return reverse("get_category", kwargs={'slug': self.full_slug})
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    
class ArticleImage(models.Model):
    image = models.ImageField(upload_to='images/', blank=False, null=False)
    article = models.ForeignKey(Article, related_name='images', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.image.name
    
    def preview(self):
        return mark_safe(f'<img src="{self.image.url}" width="100"/>')
    
class ArticleSection(models.Model):
    article = models.ForeignKey(Article, related_name='sections', on_delete=models.CASCADE, blank=False, null=False)
    title = models.CharField(max_length=300, blank=True, null=True, unique=False)
    text = models.TextField()
    quote = models.CharField(max_length=300, blank=True, null=True, unique=False)
    quote_description = models.CharField(max_length=100, blank=True, null=True, unique=False)
    highlight = models.CharField(max_length=300, blank=True, null=True, unique=False)
    

    def __str__(self):
        return self.title[:15] + ('...') if len(self.title) > 15 else ''