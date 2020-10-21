import json

from django.http import HttpResponseNotAllowed, HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet, ModelViewSet

from api_v1.serializers import ProductSerializer, OrderSerializer
from webapp.models import Product, Order


@ensure_csrf_cookie
def get_token_view(request, *args, **kwargs):
    if request.method == 'GET':
        return HttpResponse()
    return HttpResponseNotAllowed('Only GET request are allowed')


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class OrderListView(APIView):
    def get(self, request, *args, **kwargs):
        order = Order.objects.all()
        slr = OrderSerializer(order, many=True)
        return Response(slr.data)


class OrderCreateView(APIView):
    def post(self, request, *args, **kwargs):
        slr = OrderSerializer(data=request.data)
        if slr.is_valid():
            order = slr.save()
            return Response(slr.data)
        else:
            return Response(slr.errors, status=400)
