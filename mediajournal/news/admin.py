from django.contrib import admin

from .models import News

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'status']
    fields = ['title', 'status', 'author', 'text', 'published', 'cover', 'cover_preview']
    readonly_fields = ['cover_preview']
