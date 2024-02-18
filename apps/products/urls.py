from django.urls import path, \
    include  # Импортируем функции для работы с маршрутами и включения URL-маршрутов в другие URL-маршруты
from rest_framework.routers import DefaultRouter  # Импортируем дефолтный маршрутизатор Django REST Framework
from .views import ProductViewSet, BrandViewSet  # Импортируем представления ProductViewSet и BrandViewSet

# Создаем экземпляр дефолтного маршрутизатора
router = DefaultRouter()

# Регистрируем представления в маршрутизаторе
router.register('products', ProductViewSet, basename='product')  # Регистрируем представление для ресурса "products"
router.register('brands', BrandViewSet, basename='brand')  # Регистрируем представление для ресурса "brands"

# Определяем URL-маршруты для приложения
urlpatterns = [
    path('', include(router.urls)),  # Включаем URL-маршруты, сгенерированные дефолтным маршрутизатором, в корневой
    # URL-маршрут
    path('products/<int:pk>/reviews/', ProductViewSet.as_view({'get': 'reviews'}), name='product-reviews'),
    # URL для получения отзывов о продукте
    path('products/<int:pk>/like/', ProductViewSet.as_view({'post': 'like'}), name='product-like'),
    # URL для поставки лайка продукту
    path('brands/<int:pk>/products/', BrandViewSet.as_view({'get': 'products'}), name='brand-products'),
    # URL для получения продуктов конкретного бренда

]
