from django.contrib import admin
from .models import Product, Variation

class ProductAdmin (admin.ModelAdmin):
    list_display = ("name", "price", "stock", "is_available", "category")
    prepopulated_fields = {"slug": ("name",)}

class VariationAdmin (admin.ModelAdmin):
    list_display = ("product", "category", "value", "is_active")
    list_editable = ("is_active",)
    list_filter = ("product", "category", "value")

admin.site.register (Product, ProductAdmin)
admin.site.register (Variation, VariationAdmin)