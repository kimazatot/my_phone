from django.urls import path
from .views import OrderApiView, OrderConfirmView

urlpatterns = [
    path('', OrderApiView.as_view()),
    path('confirm/<int:pk>', OrderConfirmView.as_view())
]