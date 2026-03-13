from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, FishermanProfile, DriverProfile

class FishermanInline(admin.StackedInline):
    model = FishermanProfile
    can_delete = False
    extra = 0

class DriverInline(admin.StackedInline):
    model = DriverProfile
    can_delete = False
    extra = 0

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # CRITICAL: Changed 'is_verified' to 'is_verified_seller'
    list_display = ('email', 'role', 'is_verified_seller', 'is_staff')
    list_filter = ('role', 'is_verified_seller', 'is_staff')
    
    # We must redefine fieldsets because the default UserAdmin looks for 'username'
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('bio', 'location', 'phone_number', 'profile_picture')}),
        ('Permissions', {'fields': ('role', 'is_verified_seller', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    # This is required for the "Add User" form in Admin
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password', 'role'),
        }),
    )

    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()
    inlines = [FishermanInline, DriverInline]

# Remove these if they are already registered elsewhere to avoid errors
# admin.site.register(FishermanProfile)
# admin.site.register(DriverProfile)