from rest_framework import serializers
from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.name')

    class Meta:
        model = OrderItem
        fields = ('product', 'product_name', 'quantity')


class OrderSerializer(serializers.ModelSerializer):
    status = serializers.CharField(read_only=True)
    user = serializers.ReadOnlyField(source='user.email')
    products = OrderItemSerializer(write_only=True, many=True)

    class Meta:
        model = Order
        fields = '__all__'

    def create(self, validated_data):
        products = validated_data.pop('products')
        request = self.context.get('request')
        user = request.user
        total_sum = 0

        for product in products:
            try:
                total_sum += [product['quantity'] * product['product'].price]
            except:
                total_sum += product['product'].price

        order = Order.objects.create(user=user, status='in_process', total_sum=total_sum, **validated_data)

        for product in products:
            try:
                OrderItem.objects.create(order=order, product=product['product'], quantity=product['product'].quantity)
            except:
                OrderItem.objects.create(order=order, product=product['product'])

        return order

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['product'] = OrderItemSerializer(instance.items.all(), many=True).data
        return repr
