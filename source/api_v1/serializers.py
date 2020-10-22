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
        # fields = '__all__'
        fields = ['id', 'name', 'phone', 'address', 'created_at', 'user', 'order_products']
        read_only_fields = ['products']

    # def create(self, validated_data):
    #     order = Order.objects.create()
    #     order.name = validated_data['name']
    #     order.phone = validated_data['phone']
    #     order.address = validated_data['address']
    #     order.user_id = validated_data['user']
    #     # order.save()
    #     cart_products = Cart.objects.all()
    #     products = []
    #     order_products = []
    #     for item in cart_products:
    #         product = item.product
    #         qty = item.qty
    #         product.amount -= qty
    #         products.append(product)
    #         order_product = OrderProduct.objects.create(order=order, product=product, qty=qty)
    #         order_products.append(order_product)
    #     OrderProduct.objects.bulk_create(order_products)
    #     Product.objects.bulk_update(products, ('amount',))
    #     cart_products.delete()
    #     return order

#
# {
#         "name": "test",
#         "phone": "123",
#         "address": "Home",
#         "user": 2
# }