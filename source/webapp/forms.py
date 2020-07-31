from django import forms
from .models import CATEGORY_CHOICES, DEFAULT_CATEGORY


class ProductForm(forms.Form):
    name = forms.CharField(max_length=100, required=True, label='Название:')
    description = forms.CharField(max_length=2000, required=False, label='Описание товара:', widget=forms.Textarea)
    category = forms.ChoiceField(choices=CATEGORY_CHOICES, label='Категория:', initial=DEFAULT_CATEGORY)
    amount = forms.IntegerField(label='Остаток:', min_value=0, required=True)
    price = forms.DecimalField(label='Цена', required=True, max_digits=7, decimal_places=2)