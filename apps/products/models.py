from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.utils import timezone

User = get_user_model()


class Brand(models.Model):
    """
        slug (SlugField): Уникальный идентификатор бренда.
        name (CharField): Название бренда.
        user (ForeignKey): Пользователь, создавший бренд.
    """
    slug = models.SlugField(max_length=50, primary_key=True, blank=True)
    name = models.CharField(max_length=100, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='brands')

    def __str__(self):
        return self.name


class Product(models.Model):
    """
        STATUS_CHOICE (tuple): Варианты статуса товара.
        slug (SlugField): Уникальный идентификатор товара.
        name (CharField): Название товара.
        brand (CharField): Бренд товара.
        price (DecimalField): Цена товара.
        quantity (PositiveIntegerField): Количество товара в наличии.
        available (BooleanField): Доступность товара.
        description (TextField): Описание товара.
        technical_description (TextField): Техническое описание товара.
        image (ImageField): Изображение товара.
        created_at (DateTimeField): Время создания товара.
    """
    STATUS_CHOICE = (
        ('in_stock', 'В наличии'),
        ('out_of_stock', 'нет в наличии')
    )

    slug = models.SlugField(max_length=100, primary_key=True, blank=True)
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    available = models.BooleanField(default=True)
    description = models.TextField(blank=True)
    technical_description = models.TextField()
    image = models.ImageField(upload_to='product_img/', blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        """
        Переопределение метода сохранения для генерации уникального slug.
        """
        if not self.slug:
            self.slug = slugify(self.name)
        super().save()
