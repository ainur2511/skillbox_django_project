from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse_lazy, reverse
from django.utils.translation import gettext_lazy as _, gettext as __


def product_preview_image_path(instance: 'Product', filename: str) -> str:
    return 'products/product_{pk}/preview_{filename}'.format(
        pk=instance.pk,
        filename=filename,
    )


class Product(models.Model):
    """
    Модель товаров которые можно заказать или положить в корзину
    Заказы тут: :model: `shopapp.Order`
    """
    class Meta:
        ordering = ['name', 'price']
        verbose_name = _('product')
        verbose_name_plural = _('products')

    name = models.CharField(max_length=100, db_index=True)
    description = models.TextField(null=False, blank=True, db_index=True)
    price = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    discount = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    archived = models.BooleanField(default=False)
    created_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='created_product',
        null=True,
        blank=False,
        editable=False
    )
    preview = models.ImageField(null=True, blank=True, upload_to=product_preview_image_path)

    def __str__(self):
        return __(self.name)

    def get_absolute_url(self):
        return reverse('shopapp:product-detail', kwargs={'pk': self.pk})


def product_image_path(instance: 'ProductImage', filename: str) -> str:
    return 'products/product_{pk}/preview_{filename}'.format(
        pk=instance.product.pk,
        filename=filename,
    )


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=product_image_path)
    short_description = models.CharField(max_length=255, null=False, blank=True)


class Order(models.Model):
    class Meta:
        verbose_name = _('order')
        verbose_name_plural = _("orders")


    delivery_address = models.TextField(null=True, blank=True)
    promocode = models.CharField(max_length=20, null=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    products = models.ManyToManyField(Product, related_name='orders')
    receipt = models.FileField(null=True, blank=True, upload_to='orders/receipts/')

    def __str__(self):
        return __(self.delivery_address)
