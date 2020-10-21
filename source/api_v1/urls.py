from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api_v1.views import get_token_view, ProductViewSet, OrderListView, OrderCreateView

app_name = 'api_v1'

router = DefaultRouter()
router.register(r'product', ProductViewSet)

urlpatterns = [
    path('get-token/', get_token_view, name='get_token'),
    path('', include(router.urls)),
    path('orders/', OrderListView.as_view(), name='order_list'),
    path('orders/create', OrderCreateView.as_view(), name='order_create'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]