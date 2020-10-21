import json

from django.http import HttpResponseNotAllowed, HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet, ModelViewSet

from api_v1.serializers import ProductSerializer, OrderSerializer
from webapp.models import Product, Order, OrderProduct


@ensure_csrf_cookie
def get_token_view(request, *args, **kwargs):
    if request.method == 'GET':
        return HttpResponse()
    return HttpResponseNotAllowed('Only GET request are allowed')


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class OrderViewSet(ViewSet):
    queryset = Order.objects.all()

    def list(self, request):
        objects = Order.objects.all()
        slr = OrderSerializer(objects, many=True, context={'request': request})
        return Response(slr.data)

    def create(self, request):
        slr = OrderSerializer(data=request.data, context={'request': request})
        order = slr.create(request.data)
        if slr.is_valid():
            order.save()
            return Response(order)
        else:
            return Response(slr.errors, status=400)

    def retrieve(self, request, pk=None):
        object = get_object_or_404(Order, pk=pk)
        slr = OrderSerializer(object, context={'request': request})
        return Response(slr.data)