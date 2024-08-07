from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import *

class PermissionInline(admin.TabularInline):
    model = Role.permissions.through
    extra = 0

class RoleInline(admin.TabularInline):
    model = User.role.through
    extra = 0

class UserProfileInline(admin.StackedInline):  # Use StackedInline for a more compact layout
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    readonly_fields = ('user',)  # Make user read-only since it's a one-to-one field

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'phone_number', 'first_name', 'last_name', 'is_active', 'is_staff')
    search_fields = ('username', 'phone_number', 'first_name', 'last_name', 'is_verified')
    readonly_fields = ('created_at', 'updated_at')
    filter_horizontal = ()
    ordering = ('-id',)

    fieldsets = (
        (None, {'fields': ('phone_number', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'username', 'country_code')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_verified')}),
        ('Important dates', {'fields': ('last_login', 'created_at', 'updated_at')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number', 'first_name', 'last_name', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser'),
        }),
    )

    inlines = [RoleInline, UserProfileInline]

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('role', 'created_date', 'modified_date')
    search_fields = ('role',)
    inlines = [PermissionInline]

@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ('name', 'display')
    search_fields = ('name', 'display')

@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    list_display = ('user', 'otp', 'created_at', 'is_active')
    search_fields = ('user__username', 'otp')
