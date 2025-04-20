from django.contrib import admin

from .models import Bookmark

@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ['user', 'content_type', 'object_id', 'object_name']

    @admin.display(description='Title')
    def object_name(self, obj):
        return obj.content_object.title
