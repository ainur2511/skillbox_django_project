from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Group, Permission, User
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import GroupForm, OrderForm
from shopapp.models import Product, Order



class ProductsDetailsView(DetailView):
    template_name = 'shopapp/products-details.html'
    model = Product
    context_object_name = 'product'


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
    fields = ['name', 'price', 'description', 'discount']
    template_name_suffix = '_update_form'

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


class OrderCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = OrderForm
    model = Order
    success_url = reverse_lazy('shopapp:order_list')


class OrderUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    form_class = OrderForm
    model = Order
    template_name_suffix = '_update_form'

    def get_success_url(self):
        return reverse(
            'shopapp:orders_detail',
            kwargs={'pk': self.object.pk})


class OrderDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Order
    success_url = reverse_lazy('shopapp:order_list')


class OrderDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    queryset = (Order.objects.select_related('user').prefetch_related('products'))


class OrderListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    queryset = (Order.objects.select_related('user').prefetch_related('products'))
