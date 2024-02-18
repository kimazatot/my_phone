from django.db import models
from django.contrib.auth import get_user_model
from apps.products.models import Product

User = get_user_model()


class Review(models.Model):
    """
    Модель отзывов.

    Содержит информацию о комментарии, оценке, продукте, пользователе и дате создания отзыва.

    Attributes:
        comment (str): Текстовое поле для комментария.
        rating (int): Целочисленное поле для оценки (от 1 до 5).
        product (ForeignKey): Ссылка на продукт, к которому относится отзыв.
        user (ForeignKey): Ссылка на пользователя, оставившего отзыв.
        created_at (DateField): Дата создания отзыва (автоматически устанавливается при создании).
    """

    comment = models.TextField()
    rating = models.PositiveSmallIntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        """
        Возвращает строковое представление отзыва.

        Returns:
            str: Строковое представление отзыва, содержащее оценку и комментарий.
        """
        return f'{self.rating} - {self.comment}'


class Like(models.Model):
    """
    Модель лайков.

    Связывает пользователя с продуктом, который ему понравился.

    Attributes:
        product (ForeignKey): Ссылка на продукт, который был лайкнут.
        User (ForeignKey): Ссылка на пользователя, поставившего лайк.
    """

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')

    def __str__(self):
        """
        Возвращает строковое представление лайка:
        """
        return f'{self.user} liked {self.product}'
