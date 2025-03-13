from django.contrib import admin
from django.urls import reverse
from django.utils.http import urlencode
from django.utils.html import format_html

from .models import Staff, User
from articles.models import Article, Bookmark


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ['email', 'username', 'id']


class ArticleInline(admin.TabularInline):
    model = Article
    extra = 0

class BookmarkInline(admin.TabularInline):
    model = Bookmark
    extra = 0

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'phone', 'username', 'id', 'articles', 'bookmarks']
    inlines = [ArticleInline, BookmarkInline]
    
    @admin.display(description='articles')
    def articles(self, obj):
        count = obj.articles.all().count()
        url = (
            reverse('admin:articles_article_changelist')
            + '?'
            + urlencode({'author__id': obj.id})
        )
        return format_html(f'<a href="{url}">{count} articles</a>')
        
    @admin.display(description='bookmarks')
    def bookmarks(self, obj):
        count = obj.bookmarks.all().count()
        url = (
            reverse('admin:articles_bookmark_changelist')
            + '?'
            + urlencode({'user__id': obj.id})
        )
        return format_html(f'<a href="{url}">{count} bookmarks</a>')