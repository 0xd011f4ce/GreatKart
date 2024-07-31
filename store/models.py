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