from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView

from webapp.forms import CartAddForm, OrderForm
from webapp.models import Cart, Product, Order, OrderProduct

from django.contrib import messages


class CartView(ListView):
    template_name = 'order/cart_view.html'
    context_object_name = 'cart'

    def get_queryset(self):
        return Cart.get_with_product().filter(pk__in=self.get_cart_ids())

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['cart_total'] = Cart.get_cart_total(ids=self.get_cart_ids())
        context['form'] = OrderForm()
        return context

    def get_cart_ids(self):
        cart_ids = self.request.session.get('cart_ids', [])
        print(cart_ids)
        return self.request.session.get('cart_ids', [])


class CartAddView(CreateView):
    model = Cart
    form_class = CartAddForm

    def post(self, request, *args, **kwargs):
        self.product = get_object_or_404(Product, pk=self.kwargs.get('pk'))
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        qty = form.cleaned_data.get('qty', 1)

        try:
            cart_product = Cart.objects.get(product=self.product, pk__in=self.get_cart_ids())
            cart_product.qty += qty
            if cart_product.qty <= self.product.amount:
                cart_product.save()
                messages.add_message(self.request, messages.SUCCESS,
                                     f'Товар {self.product.name} ({qty}шт.) добавлен в корзину!')
            else:
                messages.add_message(self.request, messages.ERROR, 'Ошибка, невозможно добавить товар!')
        except Cart.DoesNotExist:
            if qty <= self.product.amount:
                cart_product = Cart.objects.create(product=self.product, qty=qty)
                self.save_to_session(cart_product)
                messages.add_message(self.request, messages.SUCCESS,
                                     f'Товар {self.product.name} ({qty}шт.) добавлен в корзину!')
            else:
                messages.add_message(self.request, messages.ERROR, 'Ошибка, невозможно добавить товар!')
        return redirect(self.get_success_url())

    def form_invalid(self, form):
        return redirect(self.get_success_url())

    def get_success_url(self):
        next = self.request.GET.get('next')
        if next:
            return next
        return reverse('webapp:index')

    def get_cart_ids(self):
        return self.request.session.get('cart_ids', [])

    def save_to_session(self, cart_product):
        cart_ids = self.request.session.get('cart_ids', [])
        if cart_product.pk not in cart_ids:
            cart_ids.append(cart_product.pk)
        self.request.session['cart_ids'] = cart_ids


class CartDeleteView(DeleteView):
    model = Cart
    success_url = reverse_lazy('webapp:cart_view')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.delete_from_session()
        self.object.delete()
        messages.add_message(self.request, messages.WARNING, f'Товар {self.object.product.name} удален с корзины!')
        return redirect(success_url)

    def delete_from_session(self):
        cart_ids = self.request.session.get('cart_ids', [])
        cart_ids.remove(self.object.pk)
        self.request.session['cart_ids'] = cart_ids

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)


class CartDeleteOneView(CartDeleteView):
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()

        self.object.qty -= 1
        if self.object.qty < 1:
            self.delete_from_session()
            self.object.delete()
            messages.add_message(self.request, messages.WARNING, f'Товар {self.object.product.name} удален с корзины!')
        else:
            self.object.save()
            messages.add_message(self.request, messages.WARNING,
                                 f'Количество товара {self.object.product.name} уменьшен на 1!')
        return redirect(success_url)


class OrderCreateView(CreateView):
    model = Order
    form_class = OrderForm
    success_url = reverse_lazy('webapp:index')

    def form_valid(self, form):
        response = super().form_valid(form)
        order = self.object
        cart_products = Cart.objects.all()
        products = []
        order_products = []
        if self.request.user.is_authenticated:
            user = self.request.user
            order.user = user
            order.save()
        for item in cart_products:
            product = item.product
            qty = item.qty
            product.amount -= qty
            products.append(product)
            order_product = OrderProduct(order=order, product=product, qty=qty)
            order_products.append(order_product)
        OrderProduct.objects.bulk_create(order_products)
        Product.objects.bulk_update(products, ('amount',))
        cart_products.delete()
        return response

    def form_invalid(self, form):
        return redirect('webapp:cart_view')


class OrderView(LoginRequiredMixin, ListView):
    template_name = 'order/order_view.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return Order.objects.filter(user_id=self.request.user.pk)