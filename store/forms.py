from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Photo


class SignupForm(UserCreationForm):

    class Meta:
        model=User
        fields=['username','email']


class Editpic(forms.ModelForm):
    class Meta:
        model=Photo
        fields=['title','description','image']