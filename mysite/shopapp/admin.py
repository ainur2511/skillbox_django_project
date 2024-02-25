from django.contrib import admin
from .admin_mixins import ExportAsCSVMixin

from .models import Product, Order, ProductImage
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


class ProductImageInline(admin.StackedInline):
    model = ProductImage

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin, ExportAsCSVMixin):
    actions = [mark_archived, mark_unarchived, 'export_as_csv']
    inlines = [OrderInline, ProductImageInline]
    list_display = 'pk', 'name', 'description_short', 'price', 'discount', 'archived', 'created_by'
    list_display_links = 'pk', 'name'
    ordering = 'pk',
    search_fields = 'name', 'description', 'price', 'discount'
    readonly_fields = ['created_by', 'created_at']
    fieldsets = [
        (None, {
            'fields': ('name', 'description', 'created_by', 'created_at')
        }),
        ('Price options', {
            'fields': ('price', 'discount'),
            'classes': ('collapse', 'wide')
        }),
        ('Images', {
            'fields': ('preview', ),
            'classes': ('collapse',)
        }),
        ('Extra options', {
            'fields': ('archived', ),
            'classes': ('collapse', ),
            'description': 'Extra options. Field "archived" is for soft delete',
        })

    ]
    def get_queryset(self, request):
        return Product.objects.select_related('created_by')

    def description_short(self, obj: Product) -> str:
        if len(obj.description) < 48:
            return obj.description
        return obj.description[:48] + '...'

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        obj.save()


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



