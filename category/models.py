from django.db import models
from django.utils.text import slugify

class Category(models.Model):
    category_name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)  # Allow blank for auto-generation
    description = models.TextField(max_length=255, blank=True, null=True)  # Allow null for consistency
    cat_image = models.ImageField(upload_to='photos/categories', blank=True, null=True)  # Allow null

    def save(self, *args, **kwargs):
        # Automatically generate slug if not provided
        if not self.slug:
            self.slug = slugify(self.category_name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.category_name
