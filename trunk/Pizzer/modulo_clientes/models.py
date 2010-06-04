# -*- coding: utf-8 -*-
from django.db import models
from django import forms
from django.contrib.localflavor.br.forms import BRPhoneNumberField

from modulo_funcionarios.models import Pessoa

class Cliente(Pessoa):

    class Meta:
        permissions = (
           ('pode_criar_cliente', 'Pode criar cliente'),
            ('pode_ver_todos_os_clientes', 'Pode ver todos os clientes'),
            ('pode_editar_qualquer_cliente', 'Pode editar qualquer cliente'),
            ('pode_deletar_cliente', 'Pode deletar cliente'),
        )

    def get_absolute_url(self):
        return '/pizzer/'

class ClienteForm(forms.ModelForm):
    nome = forms.RegexField(u'^([a-zA-Záéíóúãeõäëïöüç]+ )+[a-zA-Záéíóúãeõäëïöüç]+$', error_message='Nome com caracteres inválidos ou incompleto.')
    telefone = BRPhoneNumberField()

    class Meta:
        model = Cliente
        fields = ('nome', 'endereco', 'telefone')
