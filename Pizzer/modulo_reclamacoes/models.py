# -*- coding: utf-8 -*-
from django.db import models
from django import forms
from django.forms import ModelForm
from django.forms.widgets import TextInput, Textarea, Select
from modulo_clientes.models import Cliente

class Reclamacao(models.Model):  # Note que Pessoa herda da classe Model, que está dentro do módulo models
    cliente = models.ForeignKey(Cliente, null=True)  # null=True temporário até implementarem Cliente
    assunto = models.CharField(max_length=60)
    texto = models.TextField()

    class Meta:
        permissions = (
           ('pode_criar_reclamacao', 'Pode criar reclamacao'),
            ('pode_ver_reclamacoes', 'Pode ver reclamacoes'),
            ('pode_resolver_reclamacao', 'Pode resolver reclamacao'),
        )

    def __str__(self):
        return self.assunto

    def get_absolute_url(self):
        return '/pizzer/'

class ReclamacaoFormCliente(ModelForm):
    class Meta:
        model = Reclamacao

class ReclamacaoFormGerente(ModelForm):
    cliente = forms.ComboField(required=False, widget=Select(attrs={'readonly': True}))  # O Gerente só poderá editar o campo de resposta à reclamação
    assunto = forms.CharField(required=False, widget=TextInput(attrs={'readonly': True}))
    texto = forms.CharField(required=False, widget=Textarea(attrs={'readonly': True}))

    class Meta:
        model = Reclamacao
