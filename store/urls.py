from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('cart/', views.cart_view, name='cart_view'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/place-order/', views.place_order, name='place_order'),
    path('my-orders/', views.order_history_view, name='order_history'),
    path('checkout/', views.checkout, name='checkout'),
]