from django.contrib import admin
from .models import DeliveryTracking, DeliveryStatusUpdate

class DeliveryStatusUpdateInline(admin.TabularInline):
    model = DeliveryStatusUpdate
    extra = 0
    readonly_fields = ['timestamp']

@admin.register(DeliveryTracking)
class DeliveryTrackingAdmin(admin.ModelAdmin):
    list_display = ['order', 'current_location', 'updated_at']
    search_fields = ['order__order_number']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [DeliveryStatusUpdateInline]

@admin.register(DeliveryStatusUpdate)
class DeliveryStatusUpdateAdmin(admin.ModelAdmin):
    list_display = ['tracking', 'status', 'location', 'timestamp']
    list_filter = ['status', 'timestamp']
    search_fields = ['tracking__order__order_number', 'location']
    readonly_fields = ['timestamp']
