from rest_framework.serializers import ReadOnlyField, ModelSerializer, ValidationError
from .models import Product, Brand
from apps.review.serializers import ReviewSerializer
from apps.review.models import Review
from django.db.models import Avg
from django.contrib.auth import get_user_model

User = get_user_model()


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    # def validate_brand(self, brand):
    #     if not User.objects.filter(brand=brand).exists():
    #         raise ValidationError('У вас нет доступа к этому бренду.')
    #     return brand

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['reviews'] = ReviewSerializer(Review.objects.filter(product=instance.pk), many=True).data
        representation['likes'] = instance.likes.all().count()
        representation['rating'] = instance.reviews.aggregate(Avg('rating'))['rating__avg']
        return representation


class ProductListSerializer(ModelSerializer):

    class Meta:
        model = Product
        fields = ['name', 'image', 'price']

