from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_name', 'contact_number', 'payment_method', 'total_amount', 'is_paid', 'created_at')
    list_filter = ('payment_method', 'is_paid', 'created_at')
    search_fields = ('customer_name', 'contact_number', 'delivery_address')
    inlines = [OrderItemInline]

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price')
