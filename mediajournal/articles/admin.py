from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.http import urlencode

from .models import Article, Category, Comment, Bookmark, ArticleImage


class ArticleImageInline(admin.TabularInline):
    model = ArticleImage
    extra = 0
    readonly_fields = ['preview']

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    fields = ['author', 'status', 'created', 'published', 'title', 'slug', 'category', 'body', 'cover_image', 'preview', ]
    readonly_fields = ['created', 'published', 'preview']
    list_display = ['title', 'author', 'category', 'status', 'created', 'published', 'comments', 'bookmarks']
    list_filter = ['status', 'author', 'created', 'published', 'category']
    search_fields = ['title', 'body', 'author']
    ordering = ['status', '-published']
    save_on_top = True
    prepopulated_fields = {"slug": ["title",]}
    inlines = [ArticleImageInline, ]
        
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
    list_display = ['name', 'parent', 'slug', 'full_slug']
    readonly_fields = ['full_slug']
    list_filter = [('parent', admin.RelatedOnlyFieldListFilter)]
    search_fields = ['name']
    ordering = ['parent', 'name']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['short_body', 'author', 'short_title', 'created', 'is_active' ]
    list_display_links = ['short_body', 'author', 'short_title', 'created', ]
    readonly_fields = ['created']
    list_filter = ['author', 'article']
    search_fields = ['author__username', 'author__email', 'body', 'article__title']

    def short_title(self, obj):
        return obj.article.title[:15] + ('...' if len(obj.article.title) > 15 else '')
    
    def short_body(self, obj):
        return obj.body[:15] + ('...' if len(obj.body) > 15 else '')


@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ['user__email', 'article__title']
    list_filter = ['user', ]