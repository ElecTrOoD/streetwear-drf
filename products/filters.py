from django_filters import rest_framework as filters

from products.models import Product


class ProductFilter(filters.FilterSet):
    category = filters.AllValuesMultipleFilter(field_name='categories__name', label='Категории')
    color = filters.AllValuesMultipleFilter(field_name='stock__color__name', label='Цвета')
    size = filters.AllValuesMultipleFilter(field_name='stock__size__name', label='Размеры')
    gender = filters.TypedChoiceFilter(choices=Product.GENDER, label='Пол')
    price = filters.RangeFilter(field_name='price', label='Цена')

    class Meta:
        model = Product
        fields = []
