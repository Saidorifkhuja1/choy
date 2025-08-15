from rest_framework.permissions import IsAdminUser
from rest_framework import generics
from .models import Barn
from .serializers import BarnSerializer


class BarnCreateView(generics.CreateAPIView):
    queryset = Barn.objects.all()
    serializer_class = BarnSerializer
    permission_classes = [IsAdminUser]


class BarnRetrieveView(generics.RetrieveAPIView):
    queryset = Barn.objects.all()
    serializer_class = BarnSerializer
    permission_classes = [IsAdminUser]
    lookup_field = 'pk'  # Now using primary key


class BarnUpdateView(generics.UpdateAPIView):
    queryset = Barn.objects.all()
    serializer_class = BarnSerializer
    permission_classes = [IsAdminUser]
    lookup_field = 'pk'


class BarnDeleteView(generics.DestroyAPIView):
    queryset = Barn.objects.all()
    serializer_class = BarnSerializer
    permission_classes = [IsAdminUser]
    lookup_field = 'pk'


class BarnListView(generics.ListAPIView):
    queryset = Barn.objects.all()
    serializer_class = BarnSerializer
    permission_classes = [IsAdminUser]


# class BarnSearchAPIView(generics.ListAPIView):
#     serializer_class = BarnSerializer
#     permission_classes = [IsAdminUser]
#
#     def get_queryset(self):
#         queryset = Barn.objects.all()
#         name = self.request.query_params.get('name')
#         if name:
#             queryset = queryset.filter(name__icontains=name)
#         return queryset
