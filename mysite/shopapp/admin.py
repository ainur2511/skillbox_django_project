from django.contrib import admin
from .admin_mixins import ExportAsCSVMixin

from .models import Product, Order
from django.db.models import QuerySet
from django.http import HttpRequest


@admin.action(description='Archive products')
def mark_archived(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet) -> None:
    queryset.update(archived=True)


@admin.action(description='Unarchive products')
def mark_unarchived(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet) -> None:
    queryset.update(archived=False)


class OrderInline(admin.TabularInline):
    model = Product.orders.through

    def __str__(self):
        return self.verbose_name_plural


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin, ExportAsCSVMixin):
    actions = [mark_archived, mark_unarchived, 'export_as_csv']
    inlines = [OrderInline]
    list_display = 'pk', 'name', 'description_short', 'price', 'discount', 'archived'
    list_display_links = 'pk', 'name'
    ordering = 'pk',
    search_fields = 'name', 'description', 'price', 'discount'
    fieldsets = [
        (None, {
            'fields': ('name', 'description')
        }),
        ('Price options', {
            'fields': ('price', 'discount'),
            'classes': ('collapse', 'wide')
        }),
        ('Extra options', {
            'fields': ('archived', ),
            'classes': ('collapse', ),
            'description': 'Extra options. Field "archived" is for soft delete',
        })

    ]

    def description_short(self, obj: Product) -> str:
        if len(obj.description) < 48:
            return obj.description
        return obj.description[:48] + '...'


class ProductInline(admin.TabularInline):
    model = Order.products.through


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [ProductInline]
    list_display = 'delivery_address', 'promocode', 'created_at', 'user_verbose'

    def get_queryset(self, request):
        return Order.objects.select_related('user').prefetch_related('products')

    def user_verbose(self, obj: Order) -> str:
        return obj.user.first_name + ' ' + obj.user.last_name or obj.user.username
