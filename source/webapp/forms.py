from django import forms
from .models import CATEGORY_CHOICES, DEFAULT_CATEGORY


class ProductForm(forms.Form):
    name = forms.CharField(max_length=100, required=True, label='Название:',
                           widget=forms.TextInput(attrs={'class': 'form-input'}))
    description = forms.CharField(max_length=2000, required=False, label='Описание товара:',
                                  widget=forms.Textarea(attrs={'class': 'form-area'}))
    category = forms.ChoiceField(choices=CATEGORY_CHOICES, label='Категория:', initial=DEFAULT_CATEGORY,
                                 widget=forms.Select(attrs={'class': 'form-select'}))
    amount = forms.IntegerField(label='Остаток:', min_value=0, required=True,
                                widget=forms.NumberInput(attrs={'class': 'form-input'}))
    price = forms.DecimalField(label='Цена', required=True, max_digits=7, decimal_places=2,
                               widget=forms.NumberInput(attrs={'class': 'form-input'}))