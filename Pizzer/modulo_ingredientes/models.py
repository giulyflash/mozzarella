# -*- coding: utf-8 -*-
from django.db import models
from django.forms import ModelForm

class Ingrediente(models.Model):
    nome = models.CharField(max_length=25, unique=True)
    preco = models.DecimalField(max_digits=3, decimal_places=2)
    custo = models.DecimalField(max_digits=3, decimal_places=2)
    quantidade = models.IntegerField()

    def __str__(self):
        return self.nome

    def get_absolute_url(self):
        return "/pizzer/"

class IngredientesForm(ModelForm):
    class meta:
        model = Ingrediente
