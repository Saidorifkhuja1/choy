from django.urls import path
from .views import SoldProductCreateAPIView

urlpatterns = [
    path("sold-products/create/", SoldProductCreateAPIView.as_view()),
]