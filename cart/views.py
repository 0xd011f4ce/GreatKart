from django.shortcuts import render, redirect, get_object_or_404

from .models import Cart, CartItem
from store.models import Product, Variation

def _cart_get_session_id (request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create ()
    return cart

def add_cart (request, product_id):
    product = Product.objects.get (id=product_id)
    product_variations = []

    if request.method == "POST":
        for item in request.POST: # get variations
            key = item
            value = request.POST[key]

            try:
                variation = Variation.objects.get (category__iexact=key, value__iexact=value, product=product)
                product_variations.append (variation)
            except:
                pass

    try:
        cart = Cart.objects.get (cart_id=_cart_get_session_id (request)) # get the cart using the session id
    except Cart.DoesNotExist:
        cart = Cart.objects.create (cart_id=_cart_get_session_id (request))
    cart.save ()

    try:
        cart_item = CartItem.objects.get (product=product, cart=cart)
        cart_item.quantity += 1
        cart_item.save ()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create (
            product = product,
            cart = cart,
            quantity = 1
        )
        cart_item.save ()

    return redirect ("cart")

def remove_cart (request, product_id):
    cart = Cart.objects.get (cart_id=_cart_get_session_id (request))
    product = get_object_or_404 (Product, id=product_id)
    cart_item = CartItem.objects.get (product=product, cart=cart)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save ()
    else:
        cart_item.delete ()

    return redirect ("cart")

def remove_cart_item (request, product_id):
    cart = Cart.objects.get (cart_id=_cart_get_session_id (request))
    product = get_object_or_404 (Product, id=product_id)
    cart_item = CartItem.objects.get (product=product, cart=cart)
    cart_item.delete ()

    return redirect ("cart")

def cart (request, total=0, quantity=0, cart_items=None):
    try:
        tax = 0
        grand_total = 0

        cart = Cart.objects.get (cart_id=_cart_get_session_id (request))
        cart_items = CartItem.objects.filter (cart=cart, is_active=True)
        for item in cart_items:
            total += (item.product.price * item.quantity)
            quantity += item.quantity
        tax = (2 * total) / 100 # 2% tax
        grand_total = total + tax
    except Cart.DoesNotExist:
        pass

    ctx = {
        "total": total,
        "quantity": quantity,
        "cart_items": cart_items,
        "tax": tax,
        "grand_total": grand_total
    }
    return render (request, "store/cart.html", ctx)