from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from .permissions import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from .models import Product
from apps.rating.serializers import RateSerializer
from rest_framework.decorators import action, api_view
from rest_framework.pagination import PageNumberPagination


class Pagination(PageNumberPagination):
    page_size = 3
    page_query_param = 'page'


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all().order_by('created_at')
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['category', 'brand', 'price']
    search_fields = ['name', 'brand']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny]
        elif self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAuthenticated, IsBrandPermission]
        return super().get_permissions()

    # def get_serializer_class(self, *args, **kwargs):
    #     if self.action == 'list':
    #         return ProductListSerializer
    #     return self.serializer_class

    @action(['GET', 'POST', 'DELETE'], detail=True)
    def rating(self, request, pk):
        product = self.get_object()
        user = request.user
        if request.method == 'GET':
            ratings = product.ratings.all()
            serializer = RateSerializer(instance=ratings, many=True)
            return Response(serializer.data, status=200)

        elif request.method == 'POST':
            if product.ratings.filter(owner=user).exists():
                return Response('You already rated this product', status=400)
            data = request.data
            serializer = RateSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save(owner=user, product=product)
            return Response(serializer.data, status=201)

        else:
            if not product.ratings.filter(owner=user).exists():
                return Response("You didn't rated this product")
            rating = product.ratings.get(owner=user)
            rating.delete()
            return Response('Deleted', status=204)



class BrandViewSet(ModelViewSet):
    queryset = Brand.objects.all().order_by('name')
    serializer_class = BrandSerializer
    search_fields = ['name']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny]
        elif self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAuthorPermission, IsBrandPermission]
        return super().get_permissions()
