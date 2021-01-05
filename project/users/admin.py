from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationFormForStaff, CustomUserChangeFormForStaff
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationFormForStaff
    form = CustomUserChangeFormForStaff
    model = CustomUser

    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_active', 'is_cashier')
    list_filter = ('email', 'first_name', 'last_name', 'is_staff', 'is_active', 'is_cashier')

    fieldsets = (
        (None, {'fields': ('email', 'password', 'first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_cashier')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'password1', 'password2', 'is_staff', 'is_active', 'first_name', 'last_name', 'is_cashier')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)


admin.site.register(CustomUser, CustomUserAdmin)
