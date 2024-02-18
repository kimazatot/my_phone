from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, BrandViewSet

router = DefaultRouter()
router.register('products', ProductViewSet, basename='product')
router.register('brands', BrandViewSet, basename='brand')

urlpatterns = [
    path('', include(router.urls))
]