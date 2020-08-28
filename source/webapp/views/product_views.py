from django.shortcuts import render
from django.urls import reverse, reverse_lazy

from webapp.models import Product, CATEGORY_CHOICES
from webapp.forms import ProductForm
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView

from webapp.views.base_views import SearchView


class IndexView(SearchView):
    template_name = 'product/index.html'
    context_object_name = 'products'
    paginate_by = 5
    paginate_orphans = 2
    model = Product
    ordering = ['category', 'name']
    search_fields = ['name__icontains']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = CATEGORY_CHOICES
        return context

    def get_queryset(self):
        data = super().get_queryset()
        data = data.filter(amount__gt=0)
        return data


class CategoryView(SearchView):
    template_name = 'product/category_view.html'
    context_object_name = 'products'
    paginate_by = 5
    paginate_orphans = 2
    model = Product
    ordering = ['name']
    search_fields = ['name__icontains']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.kwargs.get('category')
        context['categories'] = CATEGORY_CHOICES
        return context

    def get_queryset(self):
        data = super().get_queryset()
        category = self.kwargs.get('category')
        data = data.filter(category=category)
        return data


class ProductView(DetailView):
    template_name = 'product/product_view.html'
    model = Product


class ProductCreateView(CreateView):
    template_name = 'product/product_create.html'
    form_class = ProductForm
    model = Product

    def get_success_url(self):
        return reverse('product_view', kwargs={'pk': self.object.pk})


class ProductUpdateView(UpdateView):
    template_name = 'product/product_update.html'
    form_class = ProductForm
    model = Product

    def get_success_url(self):
        return reverse('product_view', kwargs={'pk': self.object.pk})


class ProductDeleteView(DeleteView):
    template_name = 'product/product_delete.html'
    model = Product
    success_url = reverse_lazy('index')