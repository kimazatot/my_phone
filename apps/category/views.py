from django.shortcuts import render
from .models import Category
from rest_framework.viewsets import ModelViewSet
from .serializers import CategorySerializer
from rest_framework import permissions


class CategoryViewSet(ModelViewSet):
    """
        queryset (QuerySet): Набор объектов категорий.
        serializer_class (CategorySerializer): Сериализатор для категорий.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        """
        получение прав доступа на основе выполняемого действия.
        return:
            tuple: Кортеж прав доступа, зависящих от выполняемого действия.
        """
        if self.action in ('retrieve', 'list'):
            return permissions.AllowAny(),
        return permissions.IsAdminUser(),
