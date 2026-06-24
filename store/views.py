from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import Product, CartItem, Order, Wishlist, Review


def product_list(request):
    products = Product.objects.all()

    category = request.GET.get('category')

    if category:
        products = products.filter(
           category=category
        )

    search = request.GET.get('search')
    if search:
        products = products.filter(name__icontains=search)
    if request.user.is_authenticated:
        cart_count = CartItem.objects.filter(
            user=request.user
        ).count()
    else:
        cart_count = 0

    return render(request, 'store/products.html', {
        'products': products,
        'cart_count': cart_count,
        'show_cart': False,
        'show_orders': False,
    })

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.user.is_authenticated:
        cart_count = CartItem.objects.filter(user=request.user).count()
    else:
        cart_count = 0

    # STEP 2
    reviews = Review.objects.filter(product=product).order_by('-created_at')

    # STEP 3
    if request.method == "POST":
        if request.user.is_authenticated:
            rating = request.POST.get('rating')
            comment = request.POST.get('comment')

            Review.objects.create(
                product=product,
                user=request.user,
                rating=rating,
                comment=comment
            )
            return redirect('product_detail', product_id=product.id)
        else:
            return redirect('login')

    return render(request, 'store/product_detail.html', {
        'product': product,
        'cart_count': cart_count,
        'reviews': reviews
    })

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if product.stock <= 0:
        messages.error(request, "Product is out of stock")
        return redirect('product_list')

    item, created = CartItem.objects.get_or_create(
        user=request.user,
        product=product,
        defaults={'quantity': 1}
    )

    if not created:
        item.quantity += 1
        item.save()

    return redirect('cart_view')

@login_required
def buy_now(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    CartItem.objects.filter(
        user=request.user
    ).delete()

    CartItem.objects.create(
        user=request.user,
        product=product,
        quantity=1
    )

    return redirect('cart_view')

@login_required
def cart_view(request):
    cart_items = CartItem.objects.filter(
        user=request.user
    )

    total_price = sum(
        item.product.price * item.quantity
        for item in cart_items
    )
    cart_count = cart_items.count()

    return render(request, 'store/products.html', {
        'show_cart': True,
        'cart_items': cart_items,
        'total_price': total_price,
        'cart_count': cart_count,
        'show_orders': False,
    })

@login_required
def increase_quantity(request, item_id):
    item = get_object_or_404(
        CartItem,
        id=item_id,
        user=request.user
    )

    item.quantity += 1
    item.save()

    return redirect('cart_view')


@login_required
def decrease_quantity(request, item_id):
    item = get_object_or_404(
        CartItem,
        id=item_id,
        user=request.user
    )

    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()

    return redirect('cart_view')
@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(
        CartItem,
        id=item_id,
        user=request.user
        )
    item.delete()

    messages.success(request, "Item removed from cart.")
    return redirect('cart_view')


@login_required
def order_history(request):
    orders = Order.objects.filter(
        user=request.user
    ).order_by('-id')

    return render(request, 'store/products.html', {
        'show_orders': True,
        'orders': orders,
        'cart_count': CartItem.objects.filter(
            user=request.user
        ).count(),
        'show_cart': False,
    })

@login_required
def cancel_order(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user
    )

    if order.status == 'Pending':
        order.status = 'Cancelled'
        order.save()

        messages.success(
            request,
            "Order cancelled successfully."
        )

    return redirect('order_history')

@login_required
def place_order(request):
    if request.method == 'POST':

        name = request.POST.get('name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')

        # phone validation
        if len(phone) != 10 or not phone.isdigit():
            messages.error(request, "Phone number must be exactly 10 digits")
            return redirect('cart_view')

        cart_items = CartItem.objects.filter(user=request.user)

        if not cart_items.exists():
            messages.error(request, "Your cart is empty!")
            return redirect('product_list')

        total_price = sum(
            item.product.price * item.quantity
            for item in cart_items
        )

        product_names = ", ".join(
            [item.product.name for item in cart_items]
        )

        Order.objects.create(
            user=request.user,
            customer_name=name,
            customer_phone=phone,
            customer_address=address,
            product_name=product_names,
            price=total_price,
        )
        for item in cart_items:
            item.product.stock -= item.quantity
            item.product.save()

        try:
            subject = "SHA & SHA MOBILES - New Order"

            body = f"""
Customer Name: {name}
Phone: {phone}
Address: {address}

Products:
{product_names}

Total Amount: ₹{total_price}
"""

            send_mail(
                subject,
                body,
                settings.EMAIL_HOST_USER,
                [settings.EMAIL_HOST_USER],
                fail_silently=True
            )

        except Exception:
            pass

        CartItem.objects.filter(user=request.user).delete()

        messages.success(
            request,
            f"Hi {name}, your order has been placed successfully! 🎉"
        )

        return redirect('product_list')

    return redirect('cart_view')


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('register')

        User.objects.create_user(
            username=username,
            password=password
        )

        messages.success(request, "Account created successfully")
        return redirect('login')

    return render(request, 'store/register.html')


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user:
            login(request, user)
            return redirect('product_list')

        messages.error(request, "Invalid username or password")

    return render(request, 'store/login.html')

@login_required
def profile_view(request):

    orders = Order.objects.filter(user=request.user)

    total_orders = orders.count()

    total_spent = sum(
        order.price
        for order in orders
    )

    return render(request, 'store/profile.html', {
        'total_orders': total_orders,
        'total_spent': total_spent,
    })


def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def add_to_wishlist(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id
    )

    Wishlist.objects.get_or_create(
        user=request.user,
        product=product
    )

    messages.success(
        request,
        "Added to wishlist ❤️"
    )

    return redirect('product_list')
@login_required
def wishlist_view(request):

    wishlist_items = Wishlist.objects.filter(
        user=request.user
    )

    return render(
        request,
        'store/wishlist.html',
        {
            'wishlist_items': wishlist_items
        }
    )

@login_required
def remove_from_wishlist(request, item_id):
    item = get_object_or_404(
        Wishlist,
        id=item_id,
        user=request.user
    )

    item.delete()

    return redirect('wishlist')

def admin_dashboard(request):
    total_orders = Order.objects.count()
    total_products = Product.objects.count()
    total_users = User.objects.count()

    pending_orders = Order.objects.filter(status='Pending').count()

    total_revenue = 0
    orders = Order.objects.filter(status='Completed')

    for o in orders:
        total_revenue += o.total_price

    return render(request, 'store/admin_dashboard.html', {
        'total_orders': total_orders,
        'total_products': total_products,
        'total_users': total_users,
        'pending_orders': pending_orders,
        'total_revenue': total_revenue,
    })