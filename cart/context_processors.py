from .models import Cart, CartItem
from .views import _cart_get_session_id

def cart_counter (request):
    if "admin" in request.path:
        return {}

    cart_count = 0

    try:
        cart = Cart.objects.filter (cart_id=_cart_get_session_id (request))
        cart_items = CartItem.objects.all ().filter (cart=cart[:1])

        for item in cart_items:
            cart_count += item.quantity
    except Cart.DoesNotExist:
        pass
    return dict (cart_count=cart_count)