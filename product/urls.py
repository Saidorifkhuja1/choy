from django.urls import path
from .views import *

urlpatterns = [
    path('halfproducts/create/', HalfProductCreateView.as_view()),
    path('half-products/', HalfProductListView.as_view()),
    path('half-products-details/<int:pk>/', HalfProductRetrieveView.as_view()),
    path('half-products/<int:pk>/update/', HalfProductUpdateView.as_view()),
    path('half-products/<int:pk>/delete/', HalfProductDeleteView.as_view()),

    path("products_list/", ProductListAPIView.as_view()),
    path("products_create/", ProductCreateAPIView.as_view()),
    path("product_details/<int:id>/", ProductDetailAPIView.as_view()),
    path("products/<int:id>/update/", ProductUpdateAPIView.as_view()),
    path("products/<int:id>/delete/", ProductDeleteAPIView.as_view()),
]


