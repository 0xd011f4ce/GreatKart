from django.db import models

class Category (models.Model):
    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"

    name = models.CharField (max_length=32, unique=True)
    slug = models.SlugField (max_length=64, unique=True)
    description = models.TextField (blank=True)
    image = models.ImageField (upload_to="pictures/categories", blank=True)

    def __str__ (self):
        return self.name