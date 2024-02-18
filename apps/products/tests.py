from rest_framework.test import APITestCase, APIRequestFactory
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from apps.products.models import Product, Brand
from apps.products.views import ProductViewSet, BrandViewSet

User = get_user_model()


class ProductTests(APITestCase):
    """
        factory (APIRequestFactory): Фабрика запросов для создания HTTP запросов.
        user (User): Тестовый пользователь.
        brand (Brand): Тестовый бренд.
        product (Product): Тестовый продукт.
    """

    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(email='test_user@example.com', password='test_password')
        self.brand = Brand.objects.create(name='Test Brand', user=self.user)
        self.product = Product.objects.create(name='Test Product', brand=self.brand, price=10, quantity=5)

    def test_get_product_list(self):
        request = self.factory.get('/api/v1/products/')
        view = ProductViewSet.as_view({'get': 'list'})
        response = view(request)
        assert (response.status_code, 200)

    def test_create_product(self):

        data = {
            'name': 'New Product',
            'brand': self.brand.pk,
            'price': 20,
            'quantity': 10,
        }
        request = self.factory.post('/api/v1/products/', data)
        view = ProductViewSet.as_view({'post': 'create'})
        response = view(request)
        assert (response.status_code, 201)

    def test_get_product_detail(self):
        request = self.factory.get(f'/api/v1/products/{self.product.pk}/')
        view = ProductViewSet.as_view({'get': 'retrieve'})
        response = view(request, pk=self.product.pk)
        assert (response.status_code, 200)
