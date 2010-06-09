# -*- coding: utf-8 -*-
from django.db import models
from django import forms
from django.forms import ModelForm
from django.forms.widgets import TextInput, Textarea, Select
from modulo_clientes.models import Cliente

STATUS_PEDIDO_CHOICES = (
    ('A', 'Não Lida'),
    ('B', 'Em Investigação'),
    ('C', 'Incoerente'),
    ('D', 'Resolvida'),
)

class Reclamacao(models.Model):  # Note que Pessoa herda da classe Model, que está dentro do módulo models
    cliente = models.ForeignKey(Cliente, null=True)  # null=True temporário até implementarem Cliente
    assunto = models.CharField(max_length=60)
    texto = models.TextField()
    status = models.CharField(max_length=1, choices=STATUS_PEDIDO_CHOICES)

    class Meta:
        permissions = (
           ('pode_criar_reclamacao', 'Pode criar reclamacao'),
            ('pode_ver_reclamacoes', 'Pode ver reclamacoes'),
            ('pode_resolver_reclamacao', 'Pode resolver reclamacao'),
            ('pode_deletar_reclamacao', 'Pode deletar reclamacao'),
        )

    def __str__(self):
        return self.assunto

    def get_absolute_url(self):
        return '/pizzer/'

    def status_display(self):
        return Reclamacao.get_status_display(self)


class ReclamacaoFormCliente(ModelForm):
    class Meta:
        model = Reclamacao
        exclude = ['cliente', 'status']

class ReclamacaoFormGerente(ModelForm):
    class Meta:
        model = Reclamacao
        exclude = ['cliente', 'assunto', 'texto']
