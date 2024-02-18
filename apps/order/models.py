from django.db import models
from django.contrib.auth import get_user_model
from apps.products.models import Product

User = get_user_model()


class OrderItem(models.Model):
    """
        order (ForeignKey): связь с моделью заказа.
        product (ForeignKey): связь с моделью товара.
        quantity (PositiveIntegerField): количество товара.
    """
    order = models.ForeignKey('Order', related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.product.name}'


class OrderStatus(models.TextChoices):
    """
    Класс перечислений для статуса заказа.
        opened: заказ открыт.
        in_process: заказ в процессе обработки.
        completed: заказ завершен.
    """
    opened = 'opened'
    in_process = 'in_process'
    completed = 'completed'


class Order(models.Model):
    """
        user (ForeignKey): пользователь, сделавший заказ.
        product (ManyToManyField): товары в заказе.
        address (CharField): адрес доставки.
        number (CharField): номер заказа.
        status (CharField): статус заказа.
        total_sum (DecimalField): общая сумма заказа.
        created_at (DateTimeField): дата и время создания заказа.
        updated_at (DateTimeField): дата и время последнего обновления заказа.
    """
    user = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE)
    product = models.ManyToManyField(Product, through=OrderItem)
    address = models.CharField(max_length=100)
    number = models.CharField(max_length=150)
    status = models.CharField(max_length=20, choices=OrderStatus.choices, default=OrderStatus.opened)
    total_sum = models.DecimalField(max_digits=9, decimal_places=2, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user}'
