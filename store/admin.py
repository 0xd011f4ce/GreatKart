from django.contrib import admin
from .models import Product

class ProductAdmin (admin.ModelAdmin):
    list_display = ("name", "price", "stock", "is_available", "category")
    prepopulated_fields = {"slug": ("name",)}

admin.site.register (Product, ProductAdmin)