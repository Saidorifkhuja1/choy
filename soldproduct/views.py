from rest_framework import generics
from .models import SoldProduct
from .serializers import SoldProductCreateSerializer, SoldProductSerializer


class SoldProductCreateAPIView(generics.CreateAPIView):
    queryset = SoldProduct.objects.all()
    serializer_class = SoldProductCreateSerializer



class SoldProductListAPIView(generics.ListAPIView):
    queryset = SoldProduct.objects.all().order_by("-created_at")
    serializer_class = SoldProductSerializer



class SoldProductRetrieveAPIView(generics.RetrieveAPIView):
    queryset = SoldProduct.objects.all()
    serializer_class = SoldProductSerializer



class SoldProductUpdateAPIView(generics.UpdateAPIView):
    queryset = SoldProduct.objects.all()
    serializer_class = SoldProductCreateSerializer



class SoldProductDeleteAPIView(generics.DestroyAPIView):
    queryset = SoldProduct.objects.all()
    serializer_class = SoldProductSerializer
