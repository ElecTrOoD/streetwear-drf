from uuid import uuid4

from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from pytils.translit import slugify

from products.storage_backends import ImagesStorage


class Category(models.Model):
    name = models.CharField(max_length=128, unique=True, verbose_name='Название')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    GENDER = (
        ('M', 'Мужской'),
        ('F', 'Женский'),
        ('U', 'Унисекс'),
    )

    uid = models.UUIDField(primary_key=True, default=uuid4, verbose_name='Идентификатор')
    title = models.CharField(max_length=128, unique=True, verbose_name='Название')
    price = models.PositiveIntegerField(verbose_name='Цена')
    care = models.CharField(max_length=128, verbose_name='Уход')
    product_code = models.PositiveIntegerField(unique=True, verbose_name='Код товара')
    ordered = models.PositiveIntegerField(blank=True, default=0, verbose_name='Заказов')
    categories = models.ManyToManyField(Category, blank=True, verbose_name='Категории')
    slug = models.SlugField(blank=True, verbose_name='Буквенная ссылка')
    gender = models.CharField(max_length=1, choices=GENDER, default='U', verbose_name='Пол')

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Characteristic(models.Model):
    text = models.CharField(max_length=255, verbose_name='Текст')
    product_uid = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='characteristics',
                                    verbose_name='Идентификатор товара')

    class Meta:
        verbose_name = 'Характеристика'
        verbose_name_plural = 'Характеристики'

    def __str__(self):
        return self.text


class ProductImage(models.Model):
    product_uid = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images',
                                    verbose_name='Идентификатор товара')
    image = models.ImageField(storage=ImagesStorage, verbose_name='Изображение')

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'

    def delete(self, using=None, keep_parents=False):
        self.image.delete()
        super(ProductImage, self).delete()


class Color(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid4, verbose_name='Идентификатор')
    name = models.CharField(max_length=128, unique=True, verbose_name='Название')

    class Meta:
        verbose_name = 'Цвет'
        verbose_name_plural = 'Цвета'

    def __str__(self):
        return self.name


class Size(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid4, verbose_name='Идентификатор')
    name = models.CharField(max_length=128, unique=True, verbose_name='Название')

    class Meta:
        verbose_name = 'Размер'
        verbose_name_plural = 'Размеры'

    def __str__(self):
        return self.name


class ProductStock(models.Model):
    product_uid = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='stock',
                                    verbose_name='Идентификатор продукта')
    color = models.ForeignKey(Color, on_delete=models.SET_NULL, null=True, verbose_name='Цвет')
    size = models.ForeignKey(Size, on_delete=models.SET_NULL, null=True, verbose_name='Размер')
    amount = models.PositiveIntegerField(default=0, verbose_name='Запас')

    class Meta:
        verbose_name = 'Запас'
        verbose_name_plural = 'Запасы'

    def __str__(self):
        return self.product_uid.title


@receiver(pre_delete, sender=Product, dispatch_uid='product_delete_signal')
def delete_product_image_from_storage(sender, instance, using, **kwargs):
    images = instance.images.all()
    for image in images:
        image.delete()
