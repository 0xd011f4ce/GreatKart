from django.shortcuts import render

from . import models

def store (request):
    products = models.Product.objects.all ().filter (is_available = True)
    total_products = products.count ()

    ctx = {
        "products": products,
        "total_products": total_products
    }
    return render (request, "store/store.html", ctx)