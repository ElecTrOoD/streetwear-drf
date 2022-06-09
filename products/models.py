from uuid import uuid4

from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from pytils.translit import slugify

from products.storage_backends import ImagesStorage


class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid4)
    title = models.CharField(max_length=128, unique=True)
    price = models.PositiveIntegerField()
    care = models.CharField(max_length=128)
    product_code = models.PositiveIntegerField(unique=True)
    ordered = models.PositiveIntegerField(blank=True, default=0)
    categories = models.ManyToManyField(Category, blank=True)
    slug = models.SlugField(blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Characteristic(models.Model):
    text = models.CharField(max_length=255)
    product_uid = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='characteristics')

    def __str__(self):
        return self.text


class ProductImage(models.Model):
    product_uid = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(storage=ImagesStorage)

    def delete(self, using=None, keep_parents=False):
        self.image.delete()
        super(ProductImage, self).delete()


class Color(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid4)
    name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.name


class Size(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid4)
    name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.name


class ProductStock(models.Model):
    product_uid = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='stock')
    color = models.ForeignKey(Color, on_delete=models.SET_NULL, null=True)
    size = models.ForeignKey(Size, on_delete=models.SET_NULL, null=True)
    amount = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.product_uid.title


@receiver(pre_delete, sender=Product, dispatch_uid='product_delete_signal')
def delete_product_image_from_storage(sender, instance, using, **kwargs):
    images = instance.images.all()
    for image in images:
        image.delete()
