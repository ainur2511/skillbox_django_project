from django.contrib.sitemaps import Sitemap

from .models import Product


class ProductSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5

    def items(self):
        return Product.objects.all()

    def lastmod(self, obj: Product) -> str:
        return obj.created_at