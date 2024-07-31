from django.db import models
from django.urls import reverse

from category.models import Category

class Product (models.Model):
    name = models.CharField (max_length=64, unique=True)
    slug = models.SlugField (max_length=64, unique=True)
    description = models.TextField (blank=True)
    price = models.FloatField ()
    image = models.ImageField (upload_to="pictures/products")
    stock = models.IntegerField ()
    
    is_available = models.BooleanField (default=True)
    category = models.ForeignKey (Category, on_delete=models.CASCADE)
    
    creation_date = models.DateTimeField (auto_now_add=True)
    modified_date = models.DateTimeField (auto_now=True)

    def get_url (self):
        return reverse ("product_detail", args=[self.category.slug, self.slug])

    def __str__ (self):
        return self.name
    
class VariationManager (models.Manager):
    def colors (self):
        return super (VariationManager, self).filter (category="color", is_active=True)
    
    def sizes (self):
        return super (VariationManager, self).filter (category="size", is_active=True)

variation_category_choice = (
    ("color", "color"),
    ("size", "size")
)

class Variation (models.Model):
    product = models.ForeignKey (Product, on_delete=models.CASCADE)
    category = models.CharField (max_length=64, choices=variation_category_choice)
    value = models.CharField (max_length=64)

    is_active = models.BooleanField (default=True)
    created_at = models.DateTimeField (auto_now_add=True)

    objects = VariationManager ()

    def __str__ (self):
        return self.product.name + " - " + self.value