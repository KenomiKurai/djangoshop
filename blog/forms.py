from django import forms
import re
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import password_validation
from .models import Post, UserProfile, Category
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserEditForm(UserChangeForm):
    avatar = forms.ImageField(required=False)
    first_name = forms.CharField(label="Ім'я", max_length=25, required=False)
    last_name = forms.CharField(label="Прізвище", max_length=25, required=False)
    email = forms.EmailField(label="Електронна пошта", max_length=30)
    phone_number = forms.CharField(label="Телефон", max_length=15, required=False)
    group = forms.CharField(label="Група", max_length=30, required=False)
    country = forms.CharField(label="Країна", max_length=30, required=False)

    class Meta:
        model = UserProfile
        fields = ('avatar', 'first_name', 'last_name', 'email', 'phone_number', 'group', 'country')


class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=15, required=True)
    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput,
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput,
        strip=False,
        help_text="Enter the same password as before, for verification.",
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'password1', 'password2']

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")
        return password2

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ('published_date', 'user')
        fields = ['title', 'content', 'price', 'image']



class AvatarUploadForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('avatar',)
