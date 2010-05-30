# -*- coding: utf-8 -*-
from django.db import models
from django.forms import ModelForm

class Ingrediente(models.Model):
    nome = models.CharField(max_length=25, unique=True)
    preco = models.DecimalField(max_digits=4, decimal_places=2)
    quantidade = models.IntegerField()

    class Meta:
        permissions = (
           ('pode_criar_ingrediente', 'Pode criar ingrediente'),
            ('pode_ver_ingredientes', 'Pode ver ingredientes'),
            ('pode_editar_ingrediente', 'Pode editar ingrediente'),
            ('pode_deletar_pedido', 'Pode deletar pedido'),
        )

    def __str__(self):
        return self.nome

    def get_absolute_url(self):
        return "/pizzer/"

class IngredientesForm(ModelForm):
    class meta:
        model = Ingrediente
