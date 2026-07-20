from django import forms

from .models import Item


class ItemForm(forms.ModelForm):
    low_stock_threshold = forms.IntegerField(required=False, initial=5)
    category = forms.ChoiceField(
        choices=[
            ('', 'Select a category'),
            ('Electronics', 'Electronics'),
            ('Clothing', 'Clothing'),
            ('Home & Kitchen', 'Home & Kitchen'),
            ('Office Supplies', 'Office Supplies'),
            ('Health & Beauty', 'Health & Beauty'),
            ('Groceries', 'Groceries'),
            ('Tools', 'Tools'),
            ('Accessories', 'Accessories'),
        ],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Item
        fields = ['name', 'quantity', 'price', 'sku', 'category', 'supplier', 'low_stock_threshold']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'sku': forms.TextInput(attrs={'class': 'form-control'}),
            'supplier': forms.TextInput(attrs={'class': 'form-control'}),
        }
