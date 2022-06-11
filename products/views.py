from rest_framework.viewsets import ReadOnlyModelViewSet

from products.filters import ProductFilter
from products.models import Product
from products.serializers import ProductModelSerializer


class ProductModelViewSet(ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductModelSerializer
    filterset_class = ProductFilter
