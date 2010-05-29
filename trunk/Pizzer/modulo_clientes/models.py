# -*- coding: utf-8 -*-
from django.db import models
from django.forms import ModelForm

from modulo_funcionarios.models import Pessoa

class Cliente(Pessoa):
    def get_absolute_url(self):
        return '/pizzer/'

class ClienteForm(ModelForm):
    class Meta:
        model = Cliente