from rest_framework.viewsets import ModelViewSet

from products.filters import ProductFilter
from products.models import Product
from products.serializers import ProductModelSerializer


class ProductModelViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductModelSerializer
    filterset_class = ProductFilter
