from django.db import models
from apps.products.models import Product
from django.contrib.auth import get_user_model

User = get_user_model()


class Rate(models.Model):
    RATE_CHOICES = (
        (1, 'awful'),
        (2, 'bad'),
        (3, 'not so bad'),
        (4, 'good'),
        (5, 'excellent')
    )

    product = models.ForeignKey(Product, related_name='rateings', on_delete=models.CASCADE)
    owner = models.ForeignKey(User, related_name='ratings', on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(choices=RATE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинги'
        unique_together = ['owner', 'product']

