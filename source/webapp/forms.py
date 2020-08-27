from django import forms
from .models import CATEGORY_CHOICES, DEFAULT_CATEGORY, Product


class ProductForm(forms.ModelForm):
    category = forms.ChoiceField(choices=CATEGORY_CHOICES, label='Категория:', initial=DEFAULT_CATEGORY,
                                 widget=forms.Select(attrs={'class': 'form-select'}))

    class Meta:
        model = Product
        fields = ['name', 'description', 'category', 'amount', 'price']
        widgets = {'name': forms.TextInput(attrs={'class': 'form-input'}),
                   'description': forms.Textarea(attrs={'class': 'form-area'}),
                   'amount': forms.NumberInput(attrs={'class': 'form-input'}),
                   'price': forms.NumberInput(attrs={'class': 'form-input'}),
                   }


class SimpleSearchForm(forms.Form):
    search = forms.CharField(max_length=100, required=False, label="Найти")