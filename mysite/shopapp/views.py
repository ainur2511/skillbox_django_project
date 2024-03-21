import logging
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.contrib.syndication.views import Feed
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, JsonResponse
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _, ngettext_lazy as ngt
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import ModelFormMixin
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from .forms import ProductForm, OrderForm
from shopapp.models import Product, Order, ProductImage
from .serializers import ProductSerializer, OrderSerializer

logger = logging.getLogger(__name__)


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = [
        SearchFilter,
        DjangoFilterBackend,
        OrderingFilter,
    ]
    search_fields = [
        'user__username'
    ]
    filterset_fields = [
        'user__username',
        'delivery_address'
    ]
    ordering_fields = [
        'created_at',

    ]


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [
        SearchFilter,
        DjangoFilterBackend,
        OrderingFilter,
    ]
    search_fields = ['name', 'description', ]
    filterset_fields = [
        'name',
        'description',
        'price',
        'discount',
        'archived',
    ]
    ordering_fields = [
        'name',
        'description',
        'price',
        'discount',
    ]


class ProductsDetailsView(DetailView):
    template_name = 'shopapp/products-details.html'
    # model = Product
    queryset = Product.objects.prefetch_related('images')
    context_object_name = 'product'
    # logger.info('Product Details View called')


class ProductListView(ListView):
    template_name = 'shopapp/products-list.html'
    # model = Product
    context_object_name = 'products'
    queryset = Product.objects.filter(archived=False)


class ProductCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'shopapp.add_product'
    model = Product
    fields = '__all__'
    success_url = reverse_lazy('shopapp:products_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'shopapp.change_product'
    model = Product
    # fields = ['name', 'price', 'description', 'discount', 'preview']
    form_class = ProductForm
    template_name_suffix = '_update_form'

    def form_valid(self, form):
        images = form.files.getlist('images')
        for image in images:
            ProductImage.objects.create(product=self.object, image=image)
        return super(ModelFormMixin, self).form_valid(form)

    def get_success_url(self):
        return reverse(
            'shopapp:products_details',
            kwargs={'pk': self.object.pk}
        )


class ProductDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'shopapp.delete_product'
    model = Product
    success_url = reverse_lazy('shopapp:products_list')

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.archived = True
        self.object.save()
        return HttpResponseRedirect(success_url)


class LastProductsFeed(Feed):
    title = 'Shop'
    description = 'Some description'
    link = reverse_lazy('shopapp:products_list')

    def items(self):
        return Product.objects.filter(archived=False).order_by('-created_at')[:5]

    def item_title(self, item: Product) -> str:
        return item.name

    def item_description(self, item: Product) -> str:
        return item.description[:100]

class OrderCreateView(LoginRequiredMixin, CreateView):
    form_class = OrderForm
    model = Order
    success_url = reverse_lazy('shopapp:order_list')


class OrderUpdateView(LoginRequiredMixin, UpdateView):
    form_class = OrderForm
    model = Order
    template_name_suffix = '_update_form'

    def get_success_url(self):
        return reverse(
            'shopapp:orders_detail',
            kwargs={'pk': self.object.pk})


class OrderDeleteView(LoginRequiredMixin, DeleteView):
    model = Order
    success_url = reverse_lazy('shopapp:order_list')


class OrderDetailView(PermissionRequiredMixin, LoginRequiredMixin, DetailView):
    permission_required = 'shopapp.view_order'
    queryset = (Order.objects.select_related('user').prefetch_related('products'))


class OrderListView(LoginRequiredMixin, ListView):
    queryset = (Order.objects.select_related('user').prefetch_related('products'))


class OrdersDataExportView(UserPassesTestMixin, View):

    def test_func(self):
        return self.request.user.is_staff

    def get(self, request: HttpRequest) -> JsonResponse:
        orders = Order.objects.order_by('pk').all()
        orders_data = [{
            'pk': order.pk,
            'delivery_address': order.delivery_address,
            'promocode': order.promocode,
            'user': order.user.pk,
            'products': [product.pk for product in order.products.all()]
        }
            for order in orders
        ]
        return JsonResponse({'orders': orders_data})


class HelloView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        some_text = _('Hello World!')
        return HttpResponse(f'<h1>{some_text}</h1>')
