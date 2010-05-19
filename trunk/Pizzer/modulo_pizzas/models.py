# -*- coding: utf-8 -*-
from django.db import models
from django.forms import ModelForm
from modulo_clientes.models import Cliente
from modulo_ingredientes.models import Ingrediente

class ItemCardapio(models.Model):
    nome = models.CharField(max_length=25, primary_key=True)

    def __str__(self):
        return self.nome

class Pizza(ItemCardapio):
    inventor = models.ForeignKey(Cliente, null=True, blank=True)
    personalizada = models.BooleanField()
    ingredientes = models.ManyToManyField(Ingrediente)

    def __unicode__(self):
        return self.nome

    def get_absolute_url(self):
        return "/pizzer/"

class PizzaForm(ModelForm):
    class meta:
        model = Pizza