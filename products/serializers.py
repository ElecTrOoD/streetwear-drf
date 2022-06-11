from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, HyperlinkedModelSerializer

from products.models import Product, Characteristic, Category, ProductImage, ProductStock, Color


class CharacteristicModelSerializer(ModelSerializer):
    class Meta:
        model = Characteristic
        fields = ('text',)


class ProductImageModelSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = ProductImage
        fields = ('image',)


class ProductStockModelSerializer(ModelSerializer):
    color = serializers.StringRelatedField()
    size = serializers.StringRelatedField()

    class Meta:
        model = ProductStock
        fields = ('color', 'size', 'amount')


class ProductModelSerializer(ModelSerializer):
    characteristics = serializers.StringRelatedField(many=True)
    categories = serializers.StringRelatedField(many=True, required=False)
    images = ProductImageModelSerializer(many=True, required=False)
    stock = ProductStockModelSerializer(many=True)

    class Meta:
        model = Product
        fields = '__all__'
        lookup_field = 'slug'


class CategoryModelSimpleSerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ('name',)


class ColorModelSimpleSerializer(ModelSerializer):
    class Meta:
        model = Color
        fields = ('name',)


class SizeModelSimpleSerializer(ModelSerializer):
    class Meta:
        model = Color
        fields = ('name',)
