from rest_framework import generics
from .models import SoldProduct
from .serializers import SoldProductSerializer

class SoldProductCreateAPIView(generics.CreateAPIView):
    queryset = SoldProduct.objects.all()
    serializer_class = SoldProductSerializer

