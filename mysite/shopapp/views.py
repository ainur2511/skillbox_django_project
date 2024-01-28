from datetime import datetime

from django.contrib.auth.models import Group
from django.shortcuts import render
from django.http import HttpResponse, HttpRequest

from shopapp.models import Product, Order


def shop_index(request: HttpRequest):
    username = 'ainur'
    products = [
        ('Laptop', 1999),
        ('Desktop', 2999),
        ('Smartphone', 999)
    ]
    context = {
        'datetime': datetime.now(),
        'products': products,
        'username': username
    }
    return render(request, 'shopapp/shop-index.html', context=context)

def groups_list(request: HttpRequest):
    context = {
        'groups': Group.objects.prefetch_related('permissions').all()
    }
    return render(request, 'shopapp/groups-list.html', context=context)

def products_list(request: HttpRequest):
    context = {
        'products': Product.objects.all(),
    }
    return render(request, 'shopapp/products-list.html', context=context)

def orders_list(request: HttpRequest):
    context = {
        'orders': Order.objects.select_related('user').select_related('products').all()
    }
    return render(request, 'shopapp/orders-list.html', context=context)
