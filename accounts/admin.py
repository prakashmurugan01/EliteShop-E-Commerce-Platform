from django.contrib import admin
from .models import UserProfile, Address

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'created_at']
    search_fields = ['user__username', 'phone']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'user', 'city', 'is_default', 'created_at']
    list_filter = ['is_default', 'country', 'city']
    search_fields = ['full_name', 'user__username', 'street_address', 'city']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('User Info', {'fields': ('user', 'full_name', 'phone')}),
        ('Address Details', {'fields': ('street_address', 'city', 'state', 'postal_code', 'country')}),
        ('Settings', {'fields': ('is_default',)}),
        ('Timestamps', {'fields': ('created_at',), 'classes': ('collapse',)}),
    )
