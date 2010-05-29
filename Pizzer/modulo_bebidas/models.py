# -*- coding: utf-8 -*-
from django.db import models
from django.forms import ModelForm
from modulo_pizzas.models import ItemCardapio

class Bebida(ItemCardapio):
    quantidade = models.IntegerField()

    def get_absolute_url(self):
        return '/pizzer/'

class BebidaForm(ModelForm):
    class meta:
        model = Bebida
