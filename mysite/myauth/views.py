from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse, HttpRequest
from .models import Profile
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView

class AboutMeView(TemplateView):
    template_name = 'myauth/about-me.html'


class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'myauth/register.html'
    success_url = reverse_lazy('myauth:about_me')

    def form_valid(self, form):
        response = super().form_valid(form)
        Profile.objects.create(user=self.object)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(
            self.request,
            username=username,
            password=password,
        )
        login(request=self.request, user=user)
        return response



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
