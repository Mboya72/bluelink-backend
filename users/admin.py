from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, FishermanProfile, DriverProfile

class FishermanInline(admin.StackedInline):
    model = FishermanProfile
    can_delete = False

class DriverInline(admin.StackedInline):
    model = DriverProfile
    can_delete = False

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'role', 'is_verified', 'is_staff')
    list_filter = ('role', 'is_verified', 'is_staff')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('role', 'is_verified', 'is_active', 'is_staff', 'is_superuser')}),
    )
    search_fields = ('email',)
    ordering = ('email',)
    inlines = [FishermanInline, DriverInline]

admin.site.register(FishermanProfile)
admin.site.register(DriverProfile)