from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Cart, Order
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings

def product_list(request):
    products = Product.objects.all()
    search = request.GET.get('search')
    if search:
        products = products.filter(name__icontains=search)
    
    cart_count = Cart.objects.count()
    return render(request, 'store/products.html', {
        'products': products, 
        'cart_count': cart_count,
        'show_cart': False,
        'show_orders': False
    })

def cart_view(request):
    cart_items = Cart.objects.all()
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    cart_count = cart_items.count()
    return render(request, 'store/products.html', {
        'show_cart': True, 
        'cart_items': cart_items, 
        'total_price': total_price,
        'cart_count': cart_count,
        'show_orders': False
    })

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    Cart.objects.create(product=product, quantity=1)
    return redirect('cart_view')

def order_history(request):
    orders = Order.objects.all().order_by('-id')
    cart_count = Cart.objects.count()
    return render(request, 'store/products.html', {
        'show_orders': True,
        'orders': orders,
        'cart_count': cart_count,
        'show_cart': False
    })

def place_order(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        
        cart_items = Cart.objects.all()
        if not cart_items:
            messages.error(request, "Your cart is empty!")
            return redirect('product_list')
            
        total_price = sum(item.product.price * item.quantity for item in cart_items)
        product_names = ", ".join([item.product.name for item in cart_items])
        
        # 📌 FIX: Models-la irukura correct-ana table name 'Order'-ah inga track panrom!
        Order.objects.create(
            customer_name=name,
            customer_phone=phone,
            customer_address=address,
            product_name=product_names,
            price=total_price
        )
        
        # Order safe-ah database vizhundhadhum cart-ah clear panrom
        Cart.objects.all().delete()
        
        # Admin Email Notification Channel Setup
        try:
            subject = '🔥 SHA & SHA MOBILES - New Order Received!'
            body_message = f"Hi Admin,\n\nPudhusa oru customer order potrukanga!\n\nDetails:\nCustomer Name: {name}\nPhone: {phone}\nAddress: {address}\nMobiles Ordered: {product_names}\nTotal Price: ₹{total_price}\n\nCheck your Admin Panel dashboard immediately!"
            
            send_mail(
                subject,
                body_message,
                settings.EMAIL_HOST_USER,
                [settings.EMAIL_HOST_USER],
                fail_silently=False,
            )
            messages.success(request, f"Hi {name}, Unga order successfully place aayiduchu! We will reach you soon! 🎉")
        except Exception as e:
            messages.warning(request, f"Order safe-ah place aayiduchu, aana email notification anuppula: {str(e)}")
            
        return redirect('product_list')
    return redirect('cart_view')