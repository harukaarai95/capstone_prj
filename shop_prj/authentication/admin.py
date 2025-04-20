from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'role', 'is_active', 'joined_on')
    list_filter = ('role', 'is_active')
    fieldsets = BaseUserAdmin.fieldsets + (
            (None, {'fields': ('role',)}),
        )
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
            (None, {'fields': ('role',)}),
        )

admin.site.register(User, UserAdmin)