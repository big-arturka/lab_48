from django.shortcuts import render, redirect, get_object_or_404
from webapp.models import Product
from django.http import HttpResponseNotAllowed
# from webapp.forms import ProductForm


def index_view(request):
    data = Product.objects.all()
    return render(request, 'index.html', context={
        'product': data
    })


def product_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'product_view.html', context={
        'product': product})
