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
    
    # Cart database numbers tracking
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
    # Puthusa cart item add panrom
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
            
        # Total calculate panni, database-la permanent-ah permanent order records vizhuga backend create panrom
        total_price = sum(item.product.price * item.quantity for item in cart_items)
        
        # Product names details loop join variables text matrix layout config strings
        product_names = ", ".join([item.product.name for item in cart_items])
        
        # Permanent-ah Order database records-la entry vizha idho:
        Order.objects.create(
            customer_name=name,
            customer_phone=phone,
            customer_address=address,
            product_name=product_names,
            price=total_price
        )
        
        # Order backend save aanadhuku apram cart clear panrom (Delete aagadhu, order safe!)
        Cart.objects.all().delete()
        
        # Real-time Admin Email Notification Function Trigger logic setup
        try:
            subject = '🔥 SHA & SHA MOBILES - New Order Received!'
            body_message = f"Hi Admin,\n\nPudhusa oru customer order potrukanga!\n\nDetails:\nCustomer Name: {name}\nPhone: {phone}\nAddress: {address}\nMobiles Ordered: {product_names}\nTotal Price: ₹{total_price}\n\nCheck your Admin Panel dashboard status immediately!"
            
            send_mail(
                subject,
                body_message,
                settings.EMAIL_HOST_USER,
                [settings.EMAIL_HOST_USER], # Admin template configuration targets setup mail lines
                fail_silently=False,
            )
            # Live Success Feedback to Customers Alert Messages
            messages.success(request, f"Hi {name}, Unga order successfully place aayiduchu! We will reach you soon! 🎉")
        except Exception as e:
            messages.warning(request, f"Order safe-ah placed, aana Admin notification parameters load issue: {str(e)}")
            
        return redirect('product_list')
    return redirect('cart_view')