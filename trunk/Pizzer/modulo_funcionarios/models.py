# -*- coding: utf-8 -*-
from django.db import models
from django.forms import ModelForm

FUNCAO_CHOICES = (
    ('Pizzaiolo', 'Pizzaiolo'),
    ('Atendente', 'Atendente'),
    ('Gerente', 'Gerente'),
    ('Entregador', 'Entregador'),
)

PERIODO_CHOICES = (
    ('T', 'Tarde'),
    ('N', 'Noite'),
    ('N+T', 'Tarde+Noite'),
)

class Pessoa(models.Model):
    nome = models.CharField(max_length = 50)
    endereco = models.CharField(max_length = 100)
    telefone = models.CharField(max_length = 15)

    def __str__(self):  #quando o metodo str() da instancia de Funcionario e' chamado o objeto retorna o nome do funcionario
        return self.nome

    def __unicode__(self):
        return self.nome

    class Meta:
        abstract = True

class Funcionario(Pessoa):
    cpf = models.CharField(max_length = 20, primary_key = True)
    rg = models.CharField(max_length = 15)
    salario = models.DecimalField(max_digits = 10, decimal_places = 2)
    funcao = models.CharField(max_length = 10, choices = FUNCAO_CHOICES)
    periodo = models.CharField(max_length = 11, choices = PERIODO_CHOICES)

    def get_absolute_url(self): #retorna o URL absoluto da instancia de Funcionario
        return "/pizzer/"

class FuncionarioForm(ModelForm):
    class meta:
        model = Funcionario
