from django.contrib import admin

from .models import Staff, User


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ['email', 'username', 'id']

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'phone', 'username', 'id']