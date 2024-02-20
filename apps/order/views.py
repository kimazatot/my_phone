from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Order
from .serializers import OrderSerializer


class OrderApiView(ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = IsAuthenticated,

    def get(self, request, *args, **kwargs):
        user = request.user
        orders = user.orders.all()
        serializer = self.serializer_class(instance=orders, many=True)
        return Response(serializer.data, status=200)


class OrderConfirmView(APIView):
    def get(self, request, pk):
        order = Order.objects.get(pk=pk)
        order.status = 'completed'
        order.save()
        return Response({'message': 'Вы подтвердили'}, status=200)
