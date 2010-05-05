# -*- coding: utf-8 -*-
from django.db import models
from modulo_clientes.models import Cliente

# Create your models here.

class Reclamacao(models.Model):  # Note que Pessoa herda da classe Model, que está dentro do módulo models
    cliente = models.ForeignKey(Cliente, null=True, blank=True)  # null=True temporário até implementarem Cliente
    assunto = models.CharField(max_length=60)
    texto = models.TextField()

    def __str__(self):
        return self.assunto

    def get_absolute_url(self):
        return '/pizzer/'