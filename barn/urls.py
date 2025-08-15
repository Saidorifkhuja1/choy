
from django.urls import path
from .views import *

urlpatterns = [
    path('barns_lis/', BarnListView.as_view()),
    path('barnst/create/', BarnCreateView.as_view()),
    path('barns/<int:pk>/', BarnRetrieveView.as_view()),
    path('barns/<int:pk>/update/', BarnUpdateView.as_view()),
    path('barns/<int:pk>/delete/', BarnDeleteView.as_view()),
    # path('barns_search/', BarnSearchAPIView.as_view()),
]