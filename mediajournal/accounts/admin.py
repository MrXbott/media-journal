from django.contrib import admin
from django.urls import reverse
from django.utils.http import urlencode
from django.utils.html import format_html

from .models import Staff, User


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ['email', 'username', 'id']

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'phone', 'username', 'id', 'articles']
    
    @admin.display(description='articles')
    def articles(self, obj):
        count = obj.articles.all().count()
        url = (
            reverse('admin:articles_article_changelist')
            + '?'
            + urlencode({'author__id': obj.id})
        )
        return format_html(f'<a href="{url}">{count} articles</a>')