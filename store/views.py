from django.shortcuts import render, get_object_or_404

from category.models import Category
from . import models

def store (request, category_slug=None):
    categories = None
    products = None

    if category_slug != None:
        # Get the category by slug and filter products by category
        categories = get_object_or_404 (Category, slug=category_slug)
        products = models.Product.objects.filter (category=categories, is_available=True)
        total_products = products.count ()
    else:
        products = models.Product.objects.all ().filter (is_available = True)
        total_products = products.count ()

    ctx = {
        "products": products,
        "total_products": total_products
    }
    return render (request, "store/store.html", ctx)