from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from cart.views import _cart_get_session_id
from cart.models import CartItem

from category.models import Category

from . import models

def store (request, category_slug=None):
    categories = None
    products = None

    if category_slug != None:
        # Get the category by slug and filter products by category
        categories = get_object_or_404 (Category, slug=category_slug)
        products = models.Product.objects.filter (category=categories, is_available=True).order_by ("-id")
        total_products = products.count ()
    else:
        products = models.Product.objects.all ().filter (is_available = True).order_by ("-id")
        total_products = products.count ()

    paginator = Paginator (products, 6)
    page = request.GET.get ("page")
    paged_products = paginator.get_page (page)

    ctx = {
        "products": paged_products,
        "total_products": total_products
    }
    return render (request, "store/store.html", ctx)

def product_detail (request, category_slug, product_slug):
    try:
        single_product = models.Product.objects.get (category__slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter (cart__cart_id=_cart_get_session_id (request), product=single_product).exists ()
    except Exception as e:
        raise e
    
    ctx = {
        "product": single_product,
        "in_cart": in_cart
    }
    return render (request, "store/product_detail.html", ctx)

def search (request):
    if not 'query' in request.GET:
        pass # we didn't search

    query = request.GET.get ("query")
    total_products = 0
    if query:
        products = models.Product.objects.order_by ("-id").filter (Q(name__icontains=query) | Q(description__icontains=query))
        total_products = products.count ()

    ctx = {
        "products": products,
        "total_products": total_products
    }
    return render (request, "store/store.html", ctx)