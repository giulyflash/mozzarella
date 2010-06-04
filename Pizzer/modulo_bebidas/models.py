# -*- coding: utf-8 -*-
from django.db import models
from django.forms import ModelForm
from modulo_pizzas.models import ItemCardapio

class Bebida(ItemCardapio):
    quantidade = models.IntegerField()

    class Meta:
        permissions = (
           ('pode_criar_bebida', 'Pode criar bebida'),
            ('pode_ver_bebidas', 'Pode ver bebidas'),
            ('pode_editar_bebida', 'Pode editar bebida'),
            ('pode_deletar_bebida', 'Pode deletar bebida'),
        )

    def get_absolute_url(self):
        return '/pizzer/bebidas/'

class BebidaForm(ModelForm):

    class meta:
        model = Bebida
