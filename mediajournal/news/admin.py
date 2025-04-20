from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.http import urlencode
from django.contrib.contenttypes.models import ContentType


from .models import News

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'published', 'author', 'comments', 'bookmarks']
    fields = ['title', 'status', 'author', 'text', 'published', 'cover', 'cover_preview']
    readonly_fields = ['cover_preview']

    @admin.display(description='Comments')
    def comments(self, obj):
        count = obj.news_comments.count()
        content_type = ContentType.objects.get_for_model(obj)
        url = (
            reverse('admin:comments_comment_changelist')
            + '?'
            + urlencode({'object_id': obj.id, 'content_type_id': content_type.id})
        )
        return format_html(f'<a href="{url}">{count}</a>')
    
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
    
