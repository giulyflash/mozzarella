# -*- coding: utf-8 -*-

from django.contrib.auth.models import User, Group
from django import forms
from django.forms.widgets import PasswordInput

class UserCreateForm(forms.ModelForm):
    password = forms.CharField(widget=PasswordInput)
    password_r = forms.CharField(widget=PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email')

    def clean(self):
        cleaned_data = self.cleaned_data
        username= cleaned_data.get('username')
        password = cleaned_data.get('password')
        password_r = cleaned_data.get('password_r')
        if password and password_r:
            if password != password_r:
                raise forms.ValidationError('A senha e a senha repetida estão diferentes.')
        if username:
            if User.objects.filter(username=username):
                raise forms.ValidationError('O nome de usuário escolhido não está disponível.')
        return cleaned_data

class UserEditForm(forms.ModelForm):
    nova_senha = forms.CharField(max_length=15)
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        exclude = ['password']

class UserChangePassForm(forms.Form):
    password = forms.CharField(widget=PasswordInput)
    password_r = forms.CharField(widget=PasswordInput)

    def clean(self):
        cleaned_data = self.cleaned_data
        username= cleaned_data.get('username')
        password = cleaned_data.get('password')
        password_r = cleaned_data.get('password_r')
        if password and password_r:
            if password != password_r:
                raise forms.ValidationError('A senha e a senha repetida estão diferentes.')
        if username:
            if User.objects.filter(username=username):
                raise forms.ValidationError('O nome de usuário escolhido não está disponível.')
        return cleaned_data