# -*- coding: utf-8 -*-
from django.db import models
from django.forms import ModelForm

from modulo_funcionarios.models import Pessoa

class Cliente(Pessoa):

    class Meta:
        permissions = (
           ('pode_criar_cliente', 'Pode criar cliente'),
            ('pode_ver_clientes', 'Pode ver clientes'),
            ('pode_editar_cliente', 'Pode editar cliente'),
        )

    def get_absolute_url(self):
        return '/pizzer/'

class ClienteForm(ModelForm):
    class Meta:
        model = Cliente
        fields = ('nome', 'endereco', 'telefone')
