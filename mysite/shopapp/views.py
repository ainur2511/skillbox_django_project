from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, JsonResponse
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import ModelFormMixin

from .forms import ProductForm, OrderForm
from shopapp.models import Product, Order, ProductImage



class ProductsDetailsView(DetailView):
    template_name = 'shopapp/products-details.html'
    # model = Product
    context_object_name = 'product'
    queryset = Product.objects.prefetch_related('images')


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


class OrderCreateView(LoginRequiredMixin,  CreateView):
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


class OrderDeleteView(LoginRequiredMixin,  DeleteView):
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
