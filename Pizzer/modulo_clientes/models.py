# -*- coding: utf-8 -*-
from django.db import models
from django.forms import ModelForm

from modulo_funcionarios.models import Pessoa

class Cliente(Pessoa):

    class Meta:
        permissions = (
           ('pode_criar_cliente', 'Pode criar cliente'),
            ('pode_ver_todos_os_clientes', 'Pode ver todos os clientes'),
            ('pode_editar_qualquer_cliente', 'Pode editar qualquer cliente'),
            ('pode_ver_detalhes_de_cliente_com_pedido', 'Pode ver detalhes de cliente com pedido'),
            ('pode_editar_qualquer_cliente', 'Pode deletar cliente'),
        )

    def get_absolute_url(self):
        return '/pizzer/'

class ClienteForm(ModelForm):
    class Meta:
        model = Cliente
        fields = ('nome', 'endereco', 'telefone')
