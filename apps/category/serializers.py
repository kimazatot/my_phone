from rest_framework import serializers
from apps.category.models import Category


class CategorySerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Category:
        slug (ReadOnlyField): Уникальный идентификатор категории в URL (только для чтения).
    """
    slug = serializers.ReadOnlyField()  # Slug устанавливается автоматически и доступен только для чтения

    class Meta:
        model = Category
        fields = ('slug', 'name')
