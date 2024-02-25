from django.core.exceptions import PermissionDenied
from django.db.models import F
from django.views.generic.edit import ModelFormMixin

from .forms import *
from .models import Profile
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, CreateView, UpdateView, DetailView, ListView


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

# @login_required
# def edit_profile(request):
#     if request.method == 'POST':
#         user_form = UserUpdateForm(instance=request.user,
#                                    data=request.POST)
#         profile_form = ProfileUpdateForm(
#             instance=request.user.profile,
#             data=request.POST,
#             files=request.FILES)
#         if user_form.is_valid() and profile_form.is_valid():
#             user_form.save()
#             profile_form.save()
#     else:
#         user_form = UserUpdateForm(instance=request.user)
#         profile_form = ProfileUpdateForm(
#             instance=request.user.profile)
#     return render(request,
#                   'myauth/update.html',
#                   {'user_form': user_form,
#                    'profile_form': profile_form})


class Logout(LogoutView):
    next_page = reverse_lazy('myauth:login')
