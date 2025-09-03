
from django.urls import path
from .views import *

urlpatterns = [
    path('shops_list/', ShopListView.as_view()),
    path('shops/create/', ShopCreateView.as_view()),
    path('shops/<int:pk>/', ShopRetrieveView.as_view()),
    path('shops/<int:pk>/update/',ShopUpdateView.as_view()),
    path('shops/<int:pk>/delete/', ShopDeleteView.as_view()),
    # path('shops_search/', ShopSearchAPIView.as_view()),
]


