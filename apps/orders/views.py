from django.shortcuts import redirect, get_object_or_404, render
from apps.products.models import Product
from .models import Cart, CartItem, Order, OrderItem
from django.contrib.auth.decorators import login_required
from decimal import Decimal
from django.http import JsonResponse



# -----------------------------
# ADD TO CART
# -----------------------------
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    # AJAX update response
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        cart_count = cart.items.count()
        return JsonResponse({'success': True, 'cartItemCount': cart_count})

    return redirect(request.META.get('HTTP_REFERER', 'products:products1'))



# -----------------------------
# CART PAGE
# -----------------------------
@login_required
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = cart.items.all()

    subtotal = sum([item.total_price for item in items])

    tax_rate = Decimal('0.08')
    tax = (subtotal * tax_rate).quantize(Decimal('0.01'))

    total = (subtotal + tax).quantize(Decimal('0.01'))

    context = {
        'cart_items': items,
        'subtotal': subtotal,
        'tax': tax,
        'total': total,
    }
    return render(request, 'orders/cart.html', context)



# -----------------------------
# CLEAR CART
# -----------------------------
@login_required
def clear_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart.items.all().delete()

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'success': True})

    return redirect('products:products1')



# -----------------------------
# REMOVE ITEM
# -----------------------------
@login_required
def remove_item(request, product_id):
    cart = Cart.objects.get(user=request.user)
    cart_item = get_object_or_404(CartItem, cart=cart, product_id=product_id)
    cart_item.delete()
    return redirect('orders:cart')



# -----------------------------
# INCREMENT ITEM
# -----------------------------
@login_required
def increment_item(request, product_id):
    cart = Cart.objects.get(user=request.user)
    item = get_object_or_404(CartItem, cart=cart, product_id=product_id)
    item.quantity += 1
    item.save()
    return redirect('orders:cart')



# -----------------------------
# DECREMENT ITEM
# -----------------------------
@login_required
def decrement_item(request, product_id):
    cart = Cart.objects.get(user=request.user)
    item = get_object_or_404(CartItem, cart=cart, product_id=product_id)

    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()

    return redirect('orders:cart')



# -----------------------------
# CHECKOUT PAGE
# -----------------------------
@login_required
def checkout(request):
    cart = Cart.objects.get(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)

    subtotal = sum(item.product.price * item.quantity for item in cart_items)

    tax_rate = Decimal('0.08')
    tax = (subtotal * tax_rate).quantize(Decimal('0.01'))

    shipping = Decimal('0.00')   # Change if shipping needed

    total = (subtotal + tax + shipping).quantize(Decimal('0.01'))

    return render(request, 'orders/checkout.html', {
        "cart_items": cart_items,
        "subtotal": subtotal,
        "tax": tax,
        "shipping": shipping,
        "total": total,
    })



# -----------------------------
# PLACE ORDER
# -----------------------------
@login_required
def place_order(request):
    cart = Cart.objects.get(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)

    if not cart_items.exists():
        return redirect('orders:cart')

    # calculate totals
    subtotal = sum(item.product.price * item.quantity for item in cart_items)
    tax = (subtotal * Decimal('0.08')).quantize(Decimal('0.01'))
    shipping = Decimal('0.00')
    total_price = (subtotal + tax + shipping).quantize(Decimal('0.01'))

    # create order
    order = Order.objects.create(
        user=request.user,
        subtotal=subtotal,
        tax=tax,
        shipping=shipping,
        total_price=total_price,
        status="Pending"
    )

    # save order items
    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price
        )

    # clear cart
    cart_items.delete()

    return render(request, 'orders/order_success.html', {"order": order})




