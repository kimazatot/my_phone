import logging
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from apps.products.permissions import IsAuthorOrAdmin
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from .models import Product, Brand
from .serializers import ProductSerializer, BrandSerializer

logger = logging.getLogger(__name__)


class ProductViewSet(ModelViewSet):
    """
    Представление для модели Product.
    """
    queryset = Product.objects.all().order_by('created_at')
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['brand', 'price']
    search_fields = ['name', 'brand']

    def get_permissions(self):
        """
        Получает права доступа в зависимости от действия.
        """
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny]
        elif self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAuthenticated, IsAuthorOrAdmin]
        return super().get_permissions()

    def handle_exception(self, exc):
        """
        Обработчик исключений для представления.
        """
        logger.error(f'An error occurred: {exc}')

        return Response({'detail': 'An error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class BrandViewSet(ModelViewSet):
    """
    Представление для модели Brand.
    """
    queryset = Brand.objects.all().order_by('name')
    serializer_class = BrandSerializer
    search_fields = ['name']

    def get_permissions(self):
        """
        Получает права доступа в зависимости от действия.
        """
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny]
        elif self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAuthorOrAdmin]
        return super().get_permissions()
