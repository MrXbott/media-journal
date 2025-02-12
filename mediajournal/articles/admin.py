from django.contrib import admin

from .models import Article, Category, Comment


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    fields = ['author', 'status', 'created', 'published', 'title', 'category', 'body', 'slug', 'cover_image', 'preview']
    readonly_fields = ['created', 'published', 'preview']
    list_display = ['title', 'author', 'category', 'status', 'created_admin', 'published_admin']
    list_filter = ['status', 'author', 'created', 'published', 'category']
    search_fields = ['title', 'body', 'author']
    ordering = ['status', '-published']
    save_on_top = True

    @admin.display(description='created')
    def created_admin(self, obj):
        return obj.created.strftime('%d.%m.%y')
    
    @admin.display(description='published')
    def published_admin(self, obj):
        if obj.published:
            return obj.published.strftime('%d.%m.%y')
    

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
