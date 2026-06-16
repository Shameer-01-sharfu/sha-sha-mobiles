from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Product, CartItem, OrderHistory

# 1. Store Home Page with Search and Detail Modal data support
def product_list(request):
    search_query = request.GET.get('search', '')
    if search_query:
        products = Product.objects.filter(name__icontains=search_query)
    else:
        products = Product.objects.all()
        
    cart_count = CartItem.objects.count()
    return render(request, 'store/products.html', {
        'products': products,
        'cart_count': cart_count,
        'show_products': True
    })

# 2. Add Item to Cart Logic
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    # User session illadha podhu fallback safe authentication support logic
    user = request.user if request.user.is_authenticated else None
    
    cart_item, created = CartItem.objects.get_or_create(product=product, user=user)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
        
    messages.success(request, f"{product.name} added to cart!")
    return redirect('product_list')

# 3. View Cart Summary Style
def cart_view(request):
    cart_items = CartItem.objects.all()
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    cart_count = cart_items.count()
    return render(request, 'store/products.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'cart_count': cart_count,
        'show_cart': True
    })

# 4. Remove Item from Cart
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.delete()
    return redirect('cart_view')

# 5. Confirm Order & Checkout 
def place_order(request):
    if request.method == 'POST':
        name = request.POST.get('name', 'Anonymous Customer')
        phone = request.POST.get('phone', '0000000000')
        address = request.POST.get('address', 'Counter Delivery Local')
        payment_method = request.POST.get('payment_method', 'COD')
        
        cart_items = CartItem.objects.all()
        if not cart_items:
            return redirect('product_list')
            
        for item in cart_items:
            OrderHistory.objects.create(
                customer_name=name,
                customer_phone=phone,
                customer_address=address,
                product_name=item.product.name,
                price=item.product.price,
                quantity=item.quantity,
                payment_method=payment_method,
                status="Order Confirmed"
            )
        cart_items.delete()
        return redirect('order_history')
    return redirect('cart_view')

# 6. View Purchase Logs
def order_history_view(request):
    orders = OrderHistory.objects.all().order_by('-id')
    cart_count = CartItem.objects.count()
    return render(request, 'store/products.html', {
        'orders': orders,
        'cart_count': cart_count,
        'show_orders': True
    })