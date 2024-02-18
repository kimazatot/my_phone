from django.test import TestCase
from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate
from django.contrib.auth import get_user_model
from apps.category.models import Category
from apps.category.views import CategoryViewSet

User = get_user_model()

class CategoryTest(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.setup_category()
        self.user = self.setup_user()

    def setup_user(self):
        """
        Создает суперпользователя для аутентификации.

        Return:
            User: Созданный суперпользователь.
        """
        return User.objects.create_superuser('admin@gmail.com', '1')

    def setup_category(self):
        """
        Создает тестовые категории.
        """
        Category.objects.create(name='category1')
        Category.objects.create(name='category2')
        Category.objects.create(name='category3')

    def test_get_category(self):
        """
        Создает GET запрос к API для получения списка категорий и проверяет корректность ответа.
        """
        request = self.factory.get('/api/v1/category/')
        view = CategoryViewSet.as_view({'get': 'list'})
        response = view(request)
        assert response.status_code == 200
        assert Category.objects.count() == 3
        assert Category.objects.first().name == 'category1'

    def test_post_category(self):
        """
        Создает POST запрос к API для создания новой категории и проверяет корректность ответа.
        """
        data = {
            'name': 'test_category'
        }
        request = self.factory.post('/api/v1/category/', data)
        force_authenticate(request, user=self.user)
        view = CategoryViewSet.as_view({'post': 'create'})
        response = view(request)
        assert response.status_code == 201
        assert Category.objects.filter(name='test_category').exists()
