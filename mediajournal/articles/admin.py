from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.http import urlencode

from .models import Article, Category, Bookmark, ArticleImage, ArticleSection


class ArticleImageInline(admin.TabularInline):
    model = ArticleImage
    extra = 0
    readonly_fields = ['preview']

class ArticleSectionInline(admin.StackedInline):
    model = ArticleSection
    extra = 0
    

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    fields = ['author', 'status', 'created', 'published', 'title', 'slug', 'category', 'body', 'cover_image', 'preview', 'enable_comments']
    readonly_fields = ['created', 'published', 'preview']
    list_display = ['title', 'author', 'category', 'status', 'created', 'published', 'comments', 'bookmarks']
    list_filter = ['status', 'author', 'created', 'published', 'category']
    search_fields = ['title', 'body', 'author__username', 'category__name']
    ordering = ['status', '-published']
    save_on_top = True
    prepopulated_fields = {"slug": ["title",]}
    inlines = [ArticleSectionInline, ArticleImageInline]
        
    @admin.display(description='bookmarks')
    def bookmarks(self, obj):
        count = obj.bookmarked_by.all().count()
        url = (
            reverse('admin:articles_bookmark_changelist')
            + '?'
            + urlencode({'article__id': obj.id})
        )
        return format_html(f'<a href="{url}">{count}</a>')
    
    @admin.display(description='comments')
    def comments(self, obj):
        count = obj.article_comments.all().count()
        url = (
            reverse('admin:articles_comment_changelist')
            + '?'
            + urlencode({'article__id': obj.id})
        )
        return format_html(f'<a href="{url}">{count}</a>')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'slug', 'full_slug',  ]
    readonly_fields = ['full_slug']
    list_filter = [('parent', admin.RelatedOnlyFieldListFilter)]
    search_fields = ['name']
    ordering = ['parent', 'name']


@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ['user__email', 'article__title']
    list_filter = ['user', ]