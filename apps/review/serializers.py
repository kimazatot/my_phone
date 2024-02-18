from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from .models import Review, Like
from apps.products.models import Product

User = get_user_model()


class ReviewSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Review.

    Позволяет создавать, валидировать и представлять объекты Review.

    Attributes:
        user (ReadOnlyField): Поле, указывающее имя пользователя, оставившего отзыв (только для чтения).
        product (ReadOnlyField): Поле, указывающее на название продукта, к которому относится отзыв (только для чтения).

    Methods:
        validate_rating: Проверяет, что оценка находится в диапазоне от 1 до 10.
        validate_product: Проверяет, что пользователь не оставлял отзыв на этот продукт ранее.
        create: Создает новый объект Review.
    """

    user = serializers.ReadOnlyField(source='user.name')
    product = serializers.ReadOnlyField(source='product.title')

    class Meta:
        model = Review
        fields = '__all__'

    def validate_rating(self, rating):

        if not rating in range(1, 11):
            raise serializers.ValidationError('Rating can be only from 1 to 10')
        return rating

    def validate_product(self, product):

        user = self.context.get('request').user
        if self.Meta.model.objects.filter(product=product, user=user).exists():
            raise serializers.ValidationError('You have reviewed this product already')
        return product

    def create(self, validated_data):

        user = self.context.get('request').user
        product_slug = self.context['view'].kwargs.get('slug')
        product = get_object_or_404(Product, slug=product_slug)
        validated_data['product'] = product
        review = Review.objects.create(user=user, **validated_data)
        return review


class LikeSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Like.

    Позволяет создавать, валидировать и представлять объекты Like.

    Attributes:
        user (ReadOnlyField): Поле, указывающее имя пользователя, поставившего лайк (только для чтения).
        product (ReadOnlyField): Поле, указывающее на название продукта, которому был поставлен лайк (только для чтения).

    Methods:
        validate_product: Проверяет, что пользователь не ставил лайк на этот продукт ранее.
        create: Создает новый объект Like.
    """

    user = serializers.ReadOnlyField(source='user.name')
    product = serializers.ReadOnlyField(source='product.title')

    class Meta:
        model = Like
        fields = '__all__'

    def validate_product(self, product):

        user = self.context.get('request').user
        if self.Meta.model.objects.filter(product=product, user=user).exists():
            raise serializers.ValidationError('You have liked this post already')
        return product

    def create(self, validated_data):

        user = self.context.get('request').user
        product_slug = self.context['view'].kwargs.get('slug')
        product = get_object_or_404(Product, slug=product_slug)
        validated_data['product'] = product
        like = Like.objects.create(user=user, **validated_data)
        return like
