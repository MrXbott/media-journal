from django.contrib import admin

from .models import Comment

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['short_text', 'author', 'short_title', 'created', 'is_active' ]
    list_display_links = ['short_text', 'author', 'short_title', 'created', ]
    readonly_fields = ['created']
    list_filter = ['author', ]
    search_fields = ['author__username', 'author__email', 'text',]
    save_on_top = True

    def short_title(self, obj):
        return obj.content_object.title[:15] + ('...' if len(obj.content_object.title) > 15 else '')
    
    def short_text(self, obj):
        return obj.text[:15] + ('...' if len(obj.text) > 15 else '')
