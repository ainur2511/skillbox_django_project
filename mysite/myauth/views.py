from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.core.cache import cache
from django.db.models import Prefetch
from rest_framework.generics import get_object_or_404, GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from shopapp.models import Order, Product
from .forms import *
from .models import Profile
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, DetailView, ListView
from .serializers import OrderSerializer


class UsersView(ListView):
    queryset = User.objects.all()
    template_name = 'myauth/users.html'


class AboutMeView(TemplateView):
    template_name = 'myauth/about-me.html'


class AboutUserView(DetailView):
    queryset = User.objects.prefetch_related('profile')
    template_name = 'myauth/about_user.html'


class RegisterView(CreateView):
    form_class = RegistrationForm
    template_name = 'myauth/register.html'
    success_url = reverse_lazy('myauth:about_me')

    def form_valid(self, form):
        response = super().form_valid(form)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        avatar = form.cleaned_data.get('avatar')
        bio = form.cleaned_data.get('bio')
        Profile.objects.create(username=self.object, avatar=avatar, bio=bio)
        user = authenticate(
            self.request,
            username=username,
            password=password,
        )
        login(request=self.request, user=user)
        return response


class ProfileUpdateView(UpdateView):
    model = User
    queryset = User.objects.prefetch_related('profile')
    template_name = 'myauth/update.html'
    form_class = UserUpdateForm

    def get_initial(self):
        initial = super().get_initial()
        print(initial)
        initial['bio'] = self.object.profile.bio
        initial['avatar'] = self.object.profile.avatar
        print(initial)
        return initial

    def form_valid(self, form):
        response = super().form_valid(form)
        avatar = form.cleaned_data.get('avatar')
        bio = form.cleaned_data.get('bio')
        Profile.objects.filter(username=self.object.pk).update(bio=bio)
        obj = Profile.objects.get(username=self.object.pk)
        obj.avatar = avatar
        obj.save()
        return response

    def get_success_url(self):
        return reverse_lazy('myauth:about_user', kwargs={'pk': self.object.pk})

    def get_form_class(self):
        if self.request.user.is_staff or self.request.user.pk == self.object.pk:
            return UserUpdateForm
        else:
            raise PermissionDenied


class UserOrdersListView(LoginRequiredMixin, ListView):
    template_name = 'myauth/order_list.html'

    def get_queryset(self):
        self.owner = User.objects.get(pk=self.kwargs['user_id'])
        return Order.objects.filter(user=self.owner).prefetch_related('products')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['owner'] = self.owner
        return context


class Logout(LogoutView):
    next_page = reverse_lazy('myauth:login')


class UserOrdersExportView(APIView):
    def get(self, request, user_id):
        cache_key = f'user_{user_id}_orders'
        orders = cache.get(cache_key)
        if orders is None:
            user = get_object_or_404(User, pk=user_id)
            orders = Order.objects.filter(user=user).order_by('id').prefetch_related(Prefetch('products', queryset=Product.objects.only('id')))
            cache.set(cache_key, orders, timeout=20)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
    