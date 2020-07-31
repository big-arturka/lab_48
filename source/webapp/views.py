from django.shortcuts import render, redirect, get_object_or_404
from webapp.models import Product
from django.http import HttpResponseNotAllowed
from webapp.forms import ProductForm


def index_view(request):
    data = Product.objects.all()
    return render(request, 'index.html', context={
        'product': data
    })


def product_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'product_view.html', context={
        'product': product})


def product_create(request):
    if request.method == 'GET':
        return render(request, 'product_create.html',
                      context={'form': ProductForm()})
    elif request.method == 'POST':
        form = ProductForm(data=request.POST)
        if form.is_valid():
            product = Product.objects.create(**form.cleaned_data)
            return redirect('product_view', pk=product.pk)
        else:
            return render(request, 'product_create.html', context={'form': form})
    else:
        return HttpResponseNotAllowed(permitted_methods=['GET', 'POST'])


def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'GET':
        form = ProductForm(initial={'name': product.name,
                                    'description': product.description,
                                    'category': product.category,
                                    'amount': product.amount,
                                    'price': product.price})
        return render(request, 'product_update.html', context={'form': form, 'product': product})
    elif request.method == 'POST':
        form = ProductForm(data=request.POST)
        if form.is_valid():
            product.name = form.cleaned_data['name']
            product.category = form.cleaned_data['category']
            product.description = form.cleaned_data['description']
            product.amount = form.cleaned_data['amount']
            product.price = form.cleaned_data['price']
            product.save()
            return redirect('product_view', pk=product.pk)
        else:
            return render(request, 'product_update.html',
                          context={'form': form,
                                   'product': product})
    else:
        return HttpResponseNotAllowed(permitted_methods=['GET', 'POST'])


def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'GET':
        return render(request, 'product_delete.html', context={'product': product})
    elif request.method == 'POST':
        product.delete()
        return redirect('index')