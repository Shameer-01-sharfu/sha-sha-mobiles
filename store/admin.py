from django.contrib import admin
from .models import Product, CartItem, Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'customer_name',
        'customer_phone',
        'product_name',
        'price',
        'created_at'
    )

    ordering = ('-created_at',)

admin.site.register(Product)
admin.site.register(CartItem)