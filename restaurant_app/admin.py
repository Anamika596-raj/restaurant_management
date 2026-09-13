from django.contrib import admin
from .models import MenuItem, Order


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'available')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'customer_name',
        'item',
        'quantity',
        'total_price',
        'status',
        'order_date'
    )

    def total_price(self, obj):
        return obj.item.price * obj.quantity

    total_price.short_description = 'Total Price'