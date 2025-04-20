from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.http import urlencode
from django.contrib.contenttypes.models import ContentType

from .models import Article, Category, ArticleImage, ArticleSection


class ArticleImageInline(admin.TabularInline):
    model = ArticleImage
    extra = 0
    readonly_fields = ['preview']

class ArticleSectionInline(admin.StackedInline):
    model = ArticleSection
    extra = 0
    

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    fields = ['author', 'status', 'created', 'published', 'title', 'slug', 'category', 'text', 'cover', 'cover_preview', 'enable_comments']
    readonly_fields = ['created', 'published', 'cover_preview']
    list_display = ['title', 'author', 'category', 'status', 'created', 'published', 'comments', 'bookmarks']
    list_filter = ['status', 'author', 'created', 'published', 'category']
    search_fields = ['title', 'text', 'author__username', 'category__name']
    ordering = ['status', '-published']
    save_on_top = True
    prepopulated_fields = {"slug": ["title",]}
    inlines = [ArticleSectionInline, ArticleImageInline]
        
    @admin.display(description='Bookmarks')
    def bookmarks(self, obj):
        count = obj.bookmarks.count()
        content_type = ContentType.objects.get_for_model(obj)
        url = (
            reverse('admin:bookmarks_bookmark_changelist')
            + '?'
            + urlencode({'object_id': obj.id, 'content_type_id': content_type.id})
        )
        return format_html(f'<a href="{url}">{count}</a>')
    
    @admin.display(description='Comments')
    def comments(self, obj):
        count = obj.article_comments.count()
        content_type = ContentType.objects.get_for_model(obj)
        url = (
            reverse('admin:comments_comment_changelist')
            + '?'
            + urlencode({'object_id': obj.id, 'content_type_id': content_type.id})
        )
        return format_html(f'<a href="{url}">{count}</a>')

@admin.display(description='Установить избранные категории')
def set_featured_categories(modeladmin, request, queryset):
    queryset.update(is_featured=True)

@admin.display(description='Снять избранные категории')
def remove_featured_categories(modeladmin, request, queryset):
    queryset.update(is_featured=False)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'slug', 'full_slug',  'is_featured']
    readonly_fields = ['full_slug']
    list_filter = [('parent', admin.RelatedOnlyFieldListFilter)]
    search_fields = ['name']
    ordering = ['parent', 'name']
    actions = [set_featured_categories, remove_featured_categories]

