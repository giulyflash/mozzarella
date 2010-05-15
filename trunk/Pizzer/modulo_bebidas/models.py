# -*- coding: utf-8 -*-
from django.db import models
from modulo_pizzas.models import ItemCardapio

class Bebida(ItemCardapio):
    quantidade = models.IntegerField()
    def get_absolute_url(self):
        return '/pizzer/'

# Create your models here.

