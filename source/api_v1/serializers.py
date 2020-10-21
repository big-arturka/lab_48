from rest_framework import serializers
from webapp.models import Product, Order, OrderProduct


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'name', 'phone', 'address', 'created_at', 'user', 'products']

    def create(self, validated_data, *args, **kwargs):
        products = validated_data.pop('products')
        order = Order.objects.create()
        order.name = validated_data['name']
        order.phone = validated_data['phone']
        order.address = validated_data['address']
        order.user_id = validated_data['user']
        print(order)
        for product in products:
            OrderProduct.objects.create(order=order, product_id=product['product'], qty=product['qty'])
        return order

# {
#         "name": "ModeRrr",
#         "phone": "123",
#         "address": "Home",
#         "user": 2,
#         "products": [{"product": 2 ,"qty": 2}, {"product": 1, "qty": 1}]
# }