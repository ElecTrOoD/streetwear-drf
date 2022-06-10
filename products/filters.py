from django_filters import rest_framework as filters

from products.models import Product


class ProductFilter(filters.FilterSet):
    category = filters.AllValuesMultipleFilter(field_name='categories__name', label='category')
    color = filters.AllValuesFilter(field_name='stock__color__name', label='color')
    size = filters.AllValuesFilter(field_name='stock__size__name', label='size')
    price = filters.RangeFilter(field_name='price')

    class Meta:
        model = Product
        fields = []
