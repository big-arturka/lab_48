from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DeleteView
from django.views.generic.base import View

from webapp.forms import OrderForm
from webapp.models import Basket, Product


class ProductAddView(View):
    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        if Basket.objects.filter(product=product):
            basket = Basket.objects.get(product_id=pk)
            if basket.count < product.amount:
                basket.count += 1
                basket.save()
                print('Добавил')
            else:
                print('Закончились')
        else:
            if product.amount > 0:
                Basket.objects.create(product=product, count=1)
                print('Создал')
            else:
                print('Нету в наличии')
        return redirect('index')


class BasketView(ListView):
    template_name = 'basket/basket_view.html'
    model = Basket

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        basket_dict = {}
        total = 0
        for product in Basket.objects.all():
            suma = product.product.price * product.count
            basket_dict[product] = suma
            total += suma
        context['basket'] = basket_dict
        context['total'] = total
        context['form'] = OrderForm()
        return context


class BasketDeleteView(DeleteView):
    model = Basket
    success_url = reverse_lazy('basket_view')

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)
