from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User,Permission
from django import forms

class Change_password(forms.Form):
    old_pass=forms.CharField(widget=forms.PasswordInput )
    new_pass = forms.CharField(widget=forms.PasswordInput)
    confirm_new_pass = forms.CharField(widget=forms.PasswordInput)


class Forms_Create_Urls(forms.Form):
    urls=forms.CharField(widget = forms.TextInput(attrs={'readonly':'readonly'}))


