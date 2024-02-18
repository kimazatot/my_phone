from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Order
from .serializers import OrderSerializer


class OrderApiView(ListCreateAPIView):
    """
        serializer_class (OrderSerializer): Сериализатор для заказов.
        permission_classes (tuple): Кортеж классов разрешений.
    """
    serializer_class = OrderSerializer
    permission_classes = IsAuthenticated,

    def get(self, request, *args, **kwargs):
        """
            request (Request): Запрос клиента.
            *args: Дополнительные аргументы.
            **kwargs: Дополнительные именованные аргументы.

        Returns:
            Response: Ответ сервера с данными о заказах.
        """
        user = request.user
        orders = user.orders.all()
        serializer = self.serializer_class(instance=orders, many=True)
        return Response(serializer.data, status=200)


class OrderConfirmView(APIView):
    def get(self, request, pk):
        """
        Получение запроса на подтверждение заказа.

        Args:
            request (Request): Запрос клиента.
            pk (int): ID заказа.

        Returns:
            Response: Ответ сервера с сообщением об успешном подтверждении заказа.
        """
        order = Order.objects.get(pk=pk)
        order.status = 'completed'
        order.save()
        return Response({'message': 'Вы подтвердили'}, status=200)
