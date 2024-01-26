from datetime import datetime

from django.shortcuts import render
from django.http import HttpResponse, HttpRequest


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

