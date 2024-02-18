from rest_framework.response import Response  # Импортируем класс Response из модуля rest_framework.response
from .models import Product, Brand  # Импортируем модели Product и Brand из текущего пакета
from .serializers import ProductSerializer, ProductListSerializer, \
    BrandSerializer  # Импортируем сериализаторы для продуктов и брендов
from rest_framework.viewsets import ModelViewSet  # Импортируем базовый класс ModelViewSet из rest_framework.viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated  # Импортируем классы для управления правами доступа
from apps.products.permissions import IsAuthorOrAdmin  # Импортируем кастомные права доступа
from django_filters.rest_framework import DjangoFilterBackend  # Импортируем DjangoFilterBackend для фильтрации
from rest_framework.filters import SearchFilter  # Импортируем SearchFilter для поиска
from rest_framework.decorators import action  # Импортируем декоратор для создания дополнительных действий в
# представлении
from rest_framework.pagination import PageNumberPagination  # Импортируем класс для пагинации


class Pagination(PageNumberPagination):
    """
    Пагинация для представлений.
    Устанавливает количество элементов на странице и параметр запроса для номера страницы.
    """
    page_size = 20  # Устанавливаем количество элементов на странице
    page_query_param = 'page'  # Устанавливаем имя параметра запроса для номера страницы


class ProductViewSet(ModelViewSet):
    """
    Представление для модели Product.
    """
    queryset = Product.objects.all().order_by(
        'created_at')  # Задаем запрос для получения списка объектов модели Product
    serializer_class = ProductSerializer  # Указываем класс сериализатора для модели Product
    filter_backends = [DjangoFilterBackend, SearchFilter]  # Указываем фильтры для представления
    filterset_fields = ['brand', 'price']  # Указываем поля для фильтрации
    search_fields = ['name', 'brand']  # Указываем поля для поиска

    def get_permissions(self):
        """
        Получает права доступа в зависимости от действия.
        """
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny]  # Устанавливаем права доступа для просмотра списка и деталей
        elif self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAuthenticated,
                                       IsAuthorOrAdmin]  # Устанавливаем права доступа для создания, обновления, частичного обновления и удаления
        return super().get_permissions()


class BrandViewSet(ModelViewSet):
    """
    Представление для модели Brand.
    """
    queryset = Brand.objects.all().order_by('name')  # Задаем запрос для получения списка объектов модели Brand
    serializer_class = BrandSerializer  # Указываем класс сериализатора для модели Brand
    search_fields = ['name']  # Указываем поля для поиска

    def get_permissions(self):
        """
        Получает права доступа в зависимости от действия.
        """
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny]  # Устанавливаем права доступа для просмотра списка и деталей
        elif self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAuthorOrAdmin]  # Устанавливаем права доступа для создания, обновления, частичного обновления и удаления
        return super().get_permissions()
