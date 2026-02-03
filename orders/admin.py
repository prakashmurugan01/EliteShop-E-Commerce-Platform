from django.contrib import admin
from .models import Order, OrderItem, Coupon

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product', 'quantity', 'price', 'total']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'user', 'total_amount', 'status', 'created_at']
    list_filter = ['status', 'created_at', 'payment_method']
    search_fields = ['order_number', 'user__username', 'user__email']
    readonly_fields = ['order_number', 'created_at', 'updated_at', 'discount_percentage']
    inlines = [OrderItemInline]
    
    fieldsets = (
        ('Order Info', {'fields': ('order_number', 'user', 'status')}),
        ('Delivery', {'fields': ('address', 'estimated_delivery')}),
        ('Payment', {'fields': ('payment_method', 'total_amount', 'discount_amount', 'coupon_code')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )
    
    def discount_percentage(self, obj):
        if obj.discount_amount:
            return f"{(obj.discount_amount / obj.total_amount * 100):.1f}%"
        return "0%"
    discount_percentage.short_description = 'Discount %'

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'price', 'total']
    list_filter = ['order__created_at']
    search_fields = ['order__order_number', 'product__name']
    readonly_fields = ['order', 'product', 'quantity', 'price', 'total']

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'discount_percent', 'valid_from', 'valid_to', 'is_active']
    list_filter = ['is_active', 'valid_from', 'valid_to']
    search_fields = ['code']
    readonly_fields = []
    
    fieldsets = (
        ('Coupon Info', {'fields': ('code', 'discount_percent')}),
        ('Validity', {'fields': ('valid_from', 'valid_to')}),
        ('Status', {'fields': ('is_active',)}),
    )
