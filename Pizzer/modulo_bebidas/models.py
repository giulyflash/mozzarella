# -*- coding: utf-8 -*-
from django.db import models
from modulo_pizzas.models import ItemCardapio

class Bebida(ItemCardapio):
    quantidade = models.IntegerField()

# Create your models here.

