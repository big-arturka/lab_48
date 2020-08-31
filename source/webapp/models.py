from django.core.validators import MinValueValidator
from django.db import models

DEFAULT_CATEGORY = 'other'
CATEGORY_CHOICES = (
    (DEFAULT_CATEGORY, 'Разное'),
    ('food', 'Продукты питания'),
    ('household', 'Хоз товары'),
    ('toys', 'Детские игрушки'),
    ('electronics', 'Электроника'),
)


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(max_length=2000, null=True, blank=True, verbose_name='Описание')
    category = models.CharField(max_length=20, verbose_name='Категория',
                                choices=CATEGORY_CHOICES, default=DEFAULT_CATEGORY)
    amount = models.IntegerField(verbose_name='Остаток', validators=[MinValueValidator(0)])
    price = models.DecimalField(verbose_name='Цена', max_digits=7, decimal_places=2, validators=[MinValueValidator(0)])

    def __str__(self):
        return f'{self.name} - {self.amount}'

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class Basket(models.Model):
    product = models.ForeignKey('webapp.Product', related_name='baskets', on_delete=models.PROTECT, verbose_name='Товар')
    count = models.IntegerField(verbose_name='Колличество', validators=[MinValueValidator(1)])

    def __str__(self):
        return f'{self.product}-{self.count}'

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'


class Order(models.Model):
    product = models.ManyToManyField('webapp.Product', related_name='orders', through='webapp.OrderProduct',
                                     through_fields=('order', 'product'), verbose_name='Товары')
    name = models.CharField(max_length=200, verbose_name='Имя пользователя')
    phone = models.CharField(max_length=200, verbose_name='Телефона')
    address = models.CharField(max_length=200, verbose_name='Адрес')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')

    def __str__(self):
        return f'{self.id}-{self.name}'

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class OrderProduct(models.Model):
    product = models.ForeignKey('webapp.Product', related_name='product_orders', on_delete=models.CASCADE, verbose_name='Товар')
    order = models.ForeignKey('webapp.Order', related_name='order_products', on_delete=models.CASCADE, verbose_name='Заказ')
    count = models.IntegerField(verbose_name='Колличество')