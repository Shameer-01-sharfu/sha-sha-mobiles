from django.contrib import admin
from .models import Product, CartItem, Order, Wishlist
from .models import Review
admin.site.register(Wishlist)
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'customer_name',
        'product_name',
        'price',
        'status',
        'created_at'
    )
    list_filter = (
        'status',
        'created_at',
    )
    readonly_fields = (
        'customer_name',
        'customer_phone',
        'customer_address',
        'product_name',
        'price',
    )

    ordering = ('-created_at',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'category',
        'price',
        'stock',
    )
admin.site.register(CartItem)

from .models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('product__name', 'user__username', 'comment')