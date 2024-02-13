from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy


def set_cookie(request: HttpRequest) -> HttpResponse:
    response = HttpResponse('cookie set')
    response.set_cookie('fizz', 'buzz', max_age=3600)
    return response

def get_cookie(request: HttpRequest) -> HttpResponse:
    value = request.COOKIES.get('fizz', 'default cookie value')
    return HttpResponse(f'Cookie value: {value!r}')

def set_session(request: HttpRequest) -> HttpResponse:
    request.session['foobar'] = 'spameggs'
    return HttpResponse('session set')


def get_session(request: HttpRequest) -> HttpResponse:
    value = request.session.get('foobar', 'default session value')
    return HttpResponse(f'session value: {value!r}')


class Logout(LogoutView):
    next_page = reverse_lazy('myauth:login')
