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
    fields = ['author', 'status', 'created', 'published', 'title', 'category', 'body', 'slug', 'cover_image', 'preview', ]
    readonly_fields = ['created', 'published', 'preview']
    list_display = ['title', 'author', 'category', 'status', 'created_admin', 'published_admin', 'bookmarks']
    list_filter = ['status', 'author', 'created', 'published', 'category']
    search_fields = ['title', 'body', 'author']
    ordering = ['status', '-published']
    save_on_top = True
    prepopulated_fields = {"slug": ["title",]}
    inlines = [ArticleImageInline, ]

    @admin.display(description='created')
    def created_admin(self, obj):
        return obj.created.strftime('%d.%m.%y')
    
    @admin.display(description='published')
    def published_admin(self, obj):
        if obj.published:
            return obj.published.strftime('%d.%m.%y')
        
    @admin.display(description='bookmarks')
    def bookmarks(self, obj):
        count = obj.bookmarked_by.all().count()
        url = (
            reverse('admin:articles_bookmark_changelist')
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
    list_display = ['comment_name', 'created_admin']
    readonly_fields = ['created']
    list_filter = ['author', 'article']
    search_fields = ['author__username', 'author__email', 'body', 'article__title']

    @admin.display(description='Комментарий')
    def comment_name(self, obj):
        return f'{obj.author.username if obj.author else "User deleted"} - {obj.article.title}'
    
    @admin.display(description='created')
    def created_admin(self, obj):
        return obj.created.strftime('%d.%m.%y')

@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ['user__email', 'article__title']
    list_filter = ['user', ]