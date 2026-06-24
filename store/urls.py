from django.urls import path
from . import views

urlpatterns = [
    # Home / Products
    path('', views.product_list, name='product_list'),

    path('product/<int:product_id>/', views.product_detail, name='product_detail'),

    # Authentication
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    # Cart
    path('cart/', views.cart_view, name='cart_view'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('buy-now/<int:product_id>/', views.buy_now, name='buy_now'),
    path('cart/increase/<int:item_id>/', views.increase_quantity, name='increase_quantity'),
    path('cart/decrease/<int:item_id>/', views.decrease_quantity, name='decrease_quantity'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),

    # Orders
    path('checkout/place-order/', views.place_order, name='place_order'),
    path('my-orders/', views.order_history, name='order_history'),
    path('profile/', views.profile_view, name='profile'),
]