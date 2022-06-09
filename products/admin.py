from django.contrib import admin

from products.models import Product, Characteristic, Category, ProductImage, Color, Size, ProductStock


class CharacteristicInline(admin.TabularInline):
    model = Characteristic
    fields = ('text',)
    extra = 1


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    fields = ('image',)
    extra = 1


class ProductStockInline(admin.TabularInline):
    model = ProductStock
    fields = ('color', 'size', 'amount')
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'ordered', 'product_code')
    inlines = (CharacteristicInline, ProductImageInline, ProductStockInline)
    exclude = ('uid',)


@admin.register(Characteristic)
class CharacteristicsAdmin(admin.ModelAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product_uid', 'image')


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    pass


@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    pass


@admin.register(ProductStock)
class ProductStockAdmin(admin.ModelAdmin):
    list_display = ('product_uid', 'color', 'size', 'amount')
    exclude = ('uid',)
