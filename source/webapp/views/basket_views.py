from django.shortcuts import redirect, get_object_or_404
from django.views.generic import ListView
from django.views.generic.base import View

from webapp.models import Basket, Product


class ProductAddView(View):
    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        basket = Basket.objects.filter(product=product.pk)
        if basket:
            cnt = basket.count() + 1
            print(basket.count())
            print(basket)
            basket.update(count=cnt)
        else:
            Basket.objects.create(product=product, count=1)
        return redirect('index')


class BasketView(ListView):
    template_name = 'basket/basket_view.html'
    model = Basket
    context_object_name = 'basket'
