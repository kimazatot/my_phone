from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from apps.brand.models import Brand

User = get_user_model()


class Product(models.Model):
    STATUS_CHOICE = (
        ('in_stock', 'В наличии'),
        ('out_of_stock', 'Нет в наличии')
    )

    slug = models.SlugField(primary_key=True, max_length=100, blank=True)
    name = models.CharField(max_length=100)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    available = models.BooleanField(default=True)
    description = models.TextField(blank=True)
    technical_description = models.TextField()
    image = models.ImageField(upload_to='product_img/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
