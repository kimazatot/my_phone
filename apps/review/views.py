from rest_framework.viewsets import ModelViewSet
from .serializers import *
from .models import *
from rest_framework.permissions import AllowAny, IsAuthenticated
from apps.review.permissions import IsAuthorPermission


class ReviewViewSet(ModelViewSet):
    """
    Вьюсет для работы с отзывами.
        queryset (QuerySet): Запрос к модели Review для получения списка отзывов.
        serializer_class (Serializer): Сериализатор для отзывов.
    """

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny]
        elif self.action == ['create']:
            self.permission_classes = [IsAuthenticated]
        elif self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAuthorPermission]
        return super().get_permissions()


class LikeViewSet(ModelViewSet):
    """
        queryset (QuerySet): Запрос к модели Like для получения списка лайков.
        serializer_class (Serializer): Сериализатор для лайков.
    """

    queryset = Like.objects.all()
    serializer_class = LikeSerializer

    def get_permissions(self):
        """
        Определяет права доступа для различных методов API.
        """
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny]
        elif self.action == ['create']:
            self.permission_classes = [IsAuthenticated]
        elif self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAuthorPermission]
        return super().get_permissions()
