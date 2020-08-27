from django.urls import reverse, reverse_lazy

from webapp.models import Product
from webapp.forms import ProductForm
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView

from webapp.views.base_views import SearchView


class IndexView(SearchView):
    template_name = 'product/index.html'
    context_object_name = 'products'
    paginate_by = 5
    paginate_orphans = 3
    model = Product
    ordering = ['category', 'name']
    search_fields = ['name__icontains']


# def category_view(request, category):
#     product = Product.objects.filter(category=category).order_by('name')
#     if request.method == 'GET':
#         return render(request, 'category_view.html', context={
#             'product': product,
#             'category': category,
#             'categories': CATEGORY_CHOICES
#         })


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