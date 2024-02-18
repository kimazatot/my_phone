from rest_framework import serializers
from apps.rating.models import Rate


class RateSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')
    product = serializers.ReadOnlyField(source='product.name')

    class Meta:
        models = Rate
        fields = '__all__'
