from rest_framework import mixins
from rest_framework.viewsets import ReadOnlyModelViewSet, GenericViewSet

from products.filters import ProductFilter
from products.models import Product, Category, Color, Size
from products.serializers import ProductModelSerializer, SizeModelSimpleSerializer, \
    ColorModelSimpleSerializer, CategoryModelSimpleSerializer


class ProductModelViewSet(ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductModelSerializer
    filterset_class = ProductFilter


class CategoryModelListApiView(mixins.ListModelMixin, GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoryModelSimpleSerializer


class ColorModelListApiView(mixins.ListModelMixin, GenericViewSet):
    queryset = Color.objects.all()
    serializer_class = ColorModelSimpleSerializer


class SizeModelListApiView(mixins.ListModelMixin, GenericViewSet):
    queryset = Size.objects.all()
    serializer_class = SizeModelSimpleSerializer
