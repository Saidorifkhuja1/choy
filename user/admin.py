from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User
from .forms import UserCreationForm, UserChangeForm


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = (
        'phone_number', 'username', 'name', 'last_name', 'rol',
        'is_active', 'is_admin', 'is_superuser'
    )
    list_filter = ('rol', 'is_admin', 'is_active', 'is_superuser')

    fieldsets = (
        ('Personal info', {
            'fields': ('phone_number', 'username', 'password', 'name', 'last_name', 'rol')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_admin', 'is_superuser')
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'phone_number', 'username', 'name', 'last_name', 'rol',
                'password1', 'password2', 'is_active', 'is_admin', 'is_superuser'
            ),
        }),
    )

    search_fields = ('phone_number', 'username', 'name', 'last_name', 'rol')
    ordering = ('phone_number',)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)