from django.contrib import admin
from django.urls import reverse
from django.utils.http import urlencode
from django.utils.html import format_html

from .models import Staff, User
from articles.models import Article
from bookmarks.models import Bookmark


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
    list_display = ['email', 'username', 'id', 'is_active', 'articles', 'news', 'bookmarks']
    inlines = [ArticleInline, BookmarkInline]
    save_on_top = True
    
    @admin.display(description='Articles')
    def articles(self, obj):
        count = obj.articles.count()
        url = (
            reverse('admin:articles_article_changelist')
            + '?'
            + urlencode({'author__id': obj.id})
        )
        return format_html(f'<a href="{url}">{count} articles</a>')
    
    @admin.display(description='News')
    def news(self, obj):
        count = obj.news.count()
        url = (
            reverse('admin:news_news_changelist')
            + '?'
            + urlencode({'author__id': obj.id})
        )
        return format_html(f'<a href="{url}">{count} news</a>')
        
    @admin.display(description='Bookmarks')
    def bookmarks(self, obj):
        count = obj.bookmarks.count()
        url = (
            reverse('admin:bookmarks_bookmark_changelist')
            + '?'
            + urlencode({'user__id': obj.id})
        )
        return format_html(f'<a href="{url}">{count} bookmarks</a>')
