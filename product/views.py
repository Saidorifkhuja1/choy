from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from .models import HalfProduct
from rest_framework.parsers import  FormParser, MultiPartParser
from .serializers import HalfProductSerializer, HalfProductUpdateSerializer

class HalfProductCreateView(generics.CreateAPIView):
    queryset = HalfProduct.objects.all()
    serializer_class = HalfProductSerializer
    permission_classes = [IsAdminUser]
    parser_classes = [FormParser, MultiPartParser]


class HalfProductListView(generics.ListAPIView):
    queryset = HalfProduct.objects.all()
    serializer_class = HalfProductSerializer
    # permission_classes = [IsAdminUser]


class HalfProductRetrieveView(generics.RetrieveAPIView):
    queryset = HalfProduct.objects.all()
    serializer_class = HalfProductSerializer
    # permission_classes = [IsAdminUser]
    lookup_field = 'pk'


class HalfProductUpdateView(generics.UpdateAPIView):
    queryset = HalfProduct.objects.all()
    serializer_class = HalfProductUpdateSerializer
    parser_classes = [FormParser, MultiPartParser]
    # permission_classes = [IsAdminUser]
    lookup_field = 'pk'


class HalfProductDeleteView(generics.DestroyAPIView):
    queryset = HalfProduct.objects.all()
    serializer_class = HalfProductUpdateSerializer
    # permission_classes = [IsAdminUser]
    lookup_field = 'pk'