from rest_framework.permissions import IsAdminUser
from rest_framework import generics
from .models import Shop
from .serializers import ShopSerializer


class ShopCreateView(generics.CreateAPIView):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer
    # permission_classes = [IsAdminUser]


class ShopRetrieveView(generics.RetrieveAPIView):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer
    # permission_classes = [IsAdminUser]
    lookup_field = 'pk'  # Now using primary key


class ShopUpdateView(generics.UpdateAPIView):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer
    # permission_classes = [IsAdminUser]
    lookup_field = 'pk'


class ShopDeleteView(generics.DestroyAPIView):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer
    # permission_classes = [IsAdminUser]
    lookup_field = 'pk'


class ShopListView(generics.ListAPIView):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer
    # permission_classes = [IsAdminUser]


# class ShopSearchAPIView(generics.ListAPIView):
#     serializer_class = ShopSerializer
#     permission_classes = [IsAdminUser]
#
#     def get_queryset(self):
#         queryset = Shop.objects.all()
#         name = self.request.query_params.get('name')
#         if name:
#             queryset = queryset.filter(name__icontains=name)
#         return queryset
