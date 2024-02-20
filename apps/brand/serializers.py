from rest_framework.serializers import ReadOnlyField, ModelSerializer, ValidationError
from apps.brand.models import Brand
from django.contrib.auth import get_user_model

User = get_user_model()


class BrandSerializer(ModelSerializer):
    user = ReadOnlyField(source='user.name')

    class Meta:
        model = Brand
        fields = '__all__'

    def create(self, validated_data):
        user = self.context.get('request').user
        brand = Brand.objects.create(user=user, **validated_data)
        return brand
    #
    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     representation['products'] = ProductSerializer(Product.objects.filter(brand=instance.pk), many=True).data
    #     return representation
