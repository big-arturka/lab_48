from rest_framework import serializers
from webapp.models import Product, Order, OrderProduct, Cart


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class OrderProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderProduct
        fields = ['product', 'qty']


class OrderSerializer(serializers.ModelSerializer):
    order_products = OrderProductSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'name', 'phone', 'address', 'created_at', 'user', 'order_products']
        read_only_fields = ['products']
