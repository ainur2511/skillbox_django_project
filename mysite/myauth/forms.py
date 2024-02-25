from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from myauth.models import Profile


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(label='Email')
    avatar = forms.ImageField(label='Avatar')
    bio = forms.CharField(label='Bio')

    class Meta:
        model = User
        fields = ('username', 'email', 'avatar', 'bio')


class ProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('avatar', 'bio')


class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('email', 'last_name', 'first_name')

    email = forms.EmailField(label='Email')
    first_name = forms.CharField(label='First Name')
    last_name = forms.CharField(label='Last Name')
    avatar = forms.ImageField(label='Avatar')
    bio = forms.CharField(label='Bio')


