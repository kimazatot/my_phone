from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.brand.views import BrandViewSet

router = DefaultRouter()
router.register('brands', BrandViewSet, basename='brand')

urlpatterns = [
    path('', include(router.urls)),
]