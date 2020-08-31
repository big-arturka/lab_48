from django.contrib import admin
from .models import Product, Basket, Order, OrderProduct


class ProductAdmin(admin.ModelAdmin):
    list_filter = ('category',)
    list_display = ('pk', 'name', 'amount', 'price')
    list_display_links = ('pk', 'name')
    search_fields = ('name',)


class OrderAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'phone', 'address', 'created_at')
    list_display_links = ('pk', 'name')
    ordering = ('-created_at',)


admin.site.register(Product, ProductAdmin)
admin.site.register(Basket)
admin.site.register(Order, OrderAdmin)