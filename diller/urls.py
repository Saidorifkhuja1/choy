from django.urls import path
from .views import *

urlpatterns = [
    path('dillers_list/', DillerListView.as_view()),
    path('diller/create/', DillerCreateView.as_view()),
    path('diller_details/<int:pk>/', DillerRetrieveView.as_view()),
    path('diller/<int:pk>/update/', DillerUpdateView.as_view()),
    path('diller/<int:pk>/delete/', DillerDeleteView.as_view()),
    # path('diller_search/', BarnSearchAPIView.as_view()),
]