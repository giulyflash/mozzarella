# -*- coding: utf-8 -*-
from django.db import models
from django.forms import ModelForm
from django import forms
from modulo_clientes.models import Cliente
from modulo_ingredientes.models import Ingrediente

class ItemCardapio(models.Model):
    nome = models.CharField(max_length=25, unique = True, null = False)
    preco = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return self.nome

class Pizza(ItemCardapio):
    inventor = models.ForeignKey(Cliente, null=True, blank=True)
    personalizada = models.BooleanField()
    ingredientes = models.ManyToManyField(Ingrediente)

    class Meta:
        permissions = (
           ('pode_criar_pizza', 'Pode criar pizza'),
            ('pode_ver_pizzas', 'Pode ver pizzas'),
            ('pode_editar_pizza', 'Pode editar pizza'),
            ('pode_deletar_pizza', 'Pode deletar pizza'),
        )

    def __unicode__(self):
        return self.nome

    def get_absolute_url(self):
        return "/pizzer/"

class PizzaForm(ModelForm):
    nome = forms.RegexField(r'^([a-zA-Z]+ )+[a-zA-Z]+|[0-9]+$', error_message='Insira um nome v�lido (e.g. Indiana, Napolitana 2).')

    class Meta:
        model = Pizza

class PizzaPersonalizadaForm(ModelForm):
    nome = forms.RegexField(r'^([a-zA-Z]+ )+[a-zA-Z]+|[0-9]+$', error_message='Insira um nome v�lido (e.g. Indiana, Napolitana 2).')

    class Meta:
        model = Pizza
        exclude = ['inventor', 'preco', 'personalizada', 'ingredientes']

class PizzaPersonalizadaFormParaAtendente(ModelForm):
    nome = forms.RegexField(r'^([a-zA-Z]+ )+[a-zA-Z]+|[0-9]+$', error_message='Insira um nome v�lido (e.g. Indiana, Napolitana 2).')

    inventor = forms.ModelChoiceField(queryset=Cliente.objects.all(), required=True)
    class Meta:
        model = Pizza
        exclude = ['preco', 'inventor', 'personalizada', 'ingredientes']
