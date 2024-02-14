from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.utils import timezone

User = get_user_model()


class Category(models.Model):
    slug = models.SlugField(max_length=100, primary_key=True, blank=True)
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='category_img/', blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save()


class Brand(models.Model):
    slug = models.SlugField(max_length=50, primary_key=True, blank=True)
    name = models.CharField(max_length=100, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='brands')

    def __str__(self):
        return self.name


class Product(models.Model):
    slug = models.SlugField(max_length=100,primary_key=True, blank=True)
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    available = models.BooleanField(default=True)
    description = models.TextField(blank=True)
    technical_description = models.TextField()
    image = models.ImageField(upload_to='product_img/', blank=True, null=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='products')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save()
