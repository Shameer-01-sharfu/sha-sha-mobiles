from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings

from .models import Product, CartItem, Order


def product_list(request):
    products = Product.objects.all()

    search = request.GET.get('search')
    if search:
        products = products.filter(name__icontains=search)

    cart_count = CartItem.objects.count()

    return render(request, 'store/products.html', {
        'products': products,
        'cart_count': cart_count,
        'show_cart': False,
        'show_orders': False,
    })


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    item, created = CartItem.objects.get_or_create(
        product=product,
        defaults={'quantity': 1}
    )

    if not created:
        item.quantity += 1
        item.save()

    return redirect('cart_view')
def buy_now(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    CartItem.objects.all().delete()

    CartItem.objects.create(
        product=product,
        quantity=1
    )

    return redirect('cart_view')

def cart_view(request):
    cart_items = CartItem.objects.all()

    total_price = sum(
        item.product.price * item.quantity
        for item in cart_items
    )

    return render(request, 'store/products.html', {
        'show_cart': True,
        'cart_items': cart_items,
        'total_price': total_price,
        'cart_count': cart_items.count(),
        'show_orders': False,
    })


def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    item.delete()

    messages.success(request, "Item removed from cart.")
    return redirect('cart_view')


def order_history(request):
    orders = Order.objects.all().order_by('-id')

    return render(request, 'store/products.html', {
        'show_orders': True,
        'orders': orders,
        'cart_count': CartItem.objects.count(),
        'show_cart': False,
    })


def place_order(request):
    if request.method == 'POST':

        name = request.POST.get('name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')

        cart_items = CartItem.objects.all()

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
            customer_name=name,
            customer_phone=phone,
            customer_address=address,
            product_name=product_names,
            price=total_price,
        )

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

        CartItem.objects.all().delete()

        messages.success(
            request,
            f"Hi {name}, your order has been placed successfully! 🎉"
        )

        return redirect('product_list')

    return redirect('cart_view')