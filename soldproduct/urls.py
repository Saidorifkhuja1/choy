
from django.urls import path
from .views import (
    SoldProductCreateAPIView,
    SoldProductListAPIView,
    SoldProductRetrieveAPIView,
    SoldProductUpdateAPIView,
    SoldProductDeleteAPIView,
)

urlpatterns = [
    path("sold-products/", SoldProductListAPIView.as_view()),
    path("sold-products/create/", SoldProductCreateAPIView.as_view()),
    path("sold-products/<int:pk>/", SoldProductRetrieveAPIView.as_view()),
    path("sold-products/<int:pk>/update/", SoldProductUpdateAPIView.as_view()),
    path("sold-products/<int:pk>/delete/", SoldProductDeleteAPIView.as_view()),
]