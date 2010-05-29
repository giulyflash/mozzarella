# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django import forms
from django.forms.widgets import TextInput

class UserCreateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email')

class UserEditForm(forms.ModelForm):
    nova_senha = forms.CharField(max_length=15)
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        exclude = ['password']