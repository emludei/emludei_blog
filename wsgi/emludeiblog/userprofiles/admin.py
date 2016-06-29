from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User
from .forms import ProfileCreationForm


class ProfileAdmin(UserAdmin):
    add_form = ProfileCreationForm

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    list_display = UserAdmin.list_display + ('is_active',)


admin.site.register(User, ProfileAdmin)
