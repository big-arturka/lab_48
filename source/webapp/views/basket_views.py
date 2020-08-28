from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import View

from webapp.models import Basket, Product


class ProductAddView(View):
    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        Basket.objects.create(product=product, count=1)
        return redirect('index')