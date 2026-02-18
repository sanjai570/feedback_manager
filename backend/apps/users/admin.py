from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User
from .forms import UserCreationForm, UserChangeForm

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # The forms to use for creating and editing users
    add_form = UserCreationForm
    form = UserChangeForm

    # The fields to be used in displaying the User model.
    list_display = ('email', 'name', 'role', 'status')
    list_filter = ('role', 'status')
    search_fields = ('email', 'name')
    ordering = ('email',)
    
    # Fieldsets for the modification page
    fieldsets = (
        (None, {'fields': ('email',)}),
        ("Credentials", {"fields": ("password",)}),
        ('Personal Info', {'fields': ('name', 'phone')}),
        ('Permissions', {'fields': ('role', 'status')}),
    )

    # Fieldsets for the creation page
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name', 'role', 'status'),
        }),
        ("Credentials", {
            "fields": ("email", "password1", "password2")
        }),
    )
    
    filter_horizontal = ()

