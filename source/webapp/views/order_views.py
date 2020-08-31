from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import CreateView
from django.views.generic.base import View

from webapp.forms import OrderForm
from webapp.models import Order, Product, Basket, OrderProduct


class OrderCreateView(View):
    def post(self, request):
        form = OrderForm(data=request.POST)
        if form.is_valid():
            order = Order.objects.create(**form.cleaned_data)
            for product in Basket.objects.all():
                OrderProduct.objects.create(product=product.product, order=order, count=product.count)
                prod = Product.objects.get(pk=product.product.pk)
                prod.amount = prod.amount - product.count
                prod.save()
            Basket.objects.all().delete()
            return redirect('index')
        else:
            basket = Basket.objects.all()
            return render(request, 'basket/basket_view.html', context={'form': form,
                                                                       'basket': basket})
