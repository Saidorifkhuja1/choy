from rest_framework.permissions import IsAdminUser
from rest_framework import generics
from .models import Diller
from .serializers import DillerSerializer


class DillerCreateView(generics.CreateAPIView):
    queryset = Diller.objects.all()
    serializer_class = DillerSerializer
    # permission_classes = [IsAdminUser]


class DillerRetrieveView(generics.RetrieveAPIView):
    queryset = Diller.objects.all()
    serializer_class = DillerSerializer
    # permission_classes = [IsAdminUser]
    lookup_field = 'pk'  # Now using primary key


class DillerUpdateView(generics.UpdateAPIView):
    queryset = Diller.objects.all()
    serializer_class = DillerSerializer
    # permission_classes = [IsAdminUser]
    lookup_field = 'pk'


class DillerDeleteView(generics.DestroyAPIView):
    queryset = Diller.objects.all()
    serializer_class = DillerSerializer
    # permission_classes = [IsAdminUser]
    lookup_field = 'pk'


class DillerListView(generics.ListAPIView):
    queryset = Diller.objects.all()
    serializer_class = DillerSerializer
    # permission_classes = [IsAdminUser]


# class DillerSearchAPIView(generics.ListAPIView):
#     serializer_class = DillerSerializer
#     permission_classes = [IsAdminUser]
#
#     def get_queryset(self):
#         queryset = Diller.objects.all()
#         name = self.request.query_params.get('name')
#         if name:
#             queryset = queryset.filter(name__icontains=name)
#         return queryset
