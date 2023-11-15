from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms
from django.contrib.auth.models import User

from .models import Profile


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=100,
                                 required=True,
                                 widget=forms.TextInput(attrs={"class": "form-control", "Placeholder": "First name"}))

    last_name = forms.CharField(max_length=100,
                                required=True,
                                widget=forms.TextInput(attrs={"class": "form-control", "Placeholder": "Last name"}))
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={"class": "form-control", "Placeholder": "Username"}))
    email = forms.CharField(max_length=100,
                            required=True,
                            widget=forms.TextInput(attrs={"class": "form-control", "Placeholder": "Email"}))

    password1 = forms.CharField(max_length=50,
                                required=True,
                                widget=forms.PasswordInput(attrs={"class": "form-control", "Placeholder": "Password"}))
    password2 = forms.CharField(max_length=50,
                                required=True,
                                widget=forms.PasswordInput(
                                    attrs={"class": "form-control", "Placeholder": "Confirm password"}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']


class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={"class": "form-control", "Placeholder": "Username"}))

    password = forms.CharField(max_length=50,
                               required=True,
                               widget=forms.PasswordInput(attrs={"class": "form-control", "Placeholder": "Password"}))

    class Meta:
        model = User
        fields = ['username', 'password']


class ProfileForm(forms.ModelForm):
    avatar = forms.ImageField(widget=forms.FileInput())

    class Meta:
        model = Profile
        fields = ['avatar']
