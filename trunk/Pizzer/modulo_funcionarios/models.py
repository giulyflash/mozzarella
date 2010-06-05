# -*- coding: utf-8 -*-
from django.db import models
from django import forms
from django.contrib.localflavor.br.forms import BRPhoneNumberField, BRCPFField
from django.contrib.auth.models import User

FUNCAO_CHOICES = (
    ('Pizzaiolo', 'Pizzaiolo'),
    ('Atendente', 'Atendente'),
    ('Gerente', 'Gerente'),
    ('Entregador', 'Entregador'),
    ('Garçom', 'Garçom'),
)

PERIODO_CHOICES = (
    ('T', 'Tarde'),
    ('N', 'Noite'),
    ('T+N', 'Tarde+Noite'),
)

class Pessoa(models.Model):
    usuario = models.ForeignKey(User, blank=True)
    nome = models.CharField(max_length=50)
    endereco = models.CharField(max_length=100)
    telefone = models.CharField(max_length=15)

    def __str__(self):  #quando o metodo str() da instancia de Funcionario e' chamado o objeto retorna o nome do funcionario
        return self.nome

    def __unicode__(self):
        return self.nome

    def delete(self):
        self.usuario.delete()  # Ao deletar o usuário, o cliente é deletado, pois tem uma ForeignKey apontando para o usuário.

    class Meta:
        abstract = True

class Funcionario(Pessoa):
    cpf = models.CharField(max_length=20, unique=True, null=False)
    rg = models.CharField(max_length=15)
    salario = models.DecimalField(max_digits=10, decimal_places=2)
    funcao = models.CharField(max_length=10, choices=FUNCAO_CHOICES)
    periodo = models.CharField(max_length=11, choices=PERIODO_CHOICES)

    class Meta:
        permissions = (
           ('pode_criar_funcionario', 'Pode criar funcionario'),
            ('pode_ver_funcionarios', 'Pode ver funcionarios'),
            ('pode_editar_qualquer_funcionario', 'Pode editar qualquer funcionario'),
            ('pode_deletar_funcionario', 'Pode deletar funcionario'),
        )

    def get_absolute_url(self): #retorna o URL absoluto da instancia de Funcionario
        return "/pizzer/"

    def periodo_display(self):
        return Funcionario.get_periodo_display(self)

class FuncionarioForm(forms.ModelForm):
    nome = forms.RegexField(u'^([a-zA-Záéíóúãeõäëïöüç]+ )+[a-zA-Záéíóúãeõäëïöüç]+$', error_message='Nome com caracteres inválidos ou incompleto.')
    rg = forms.CharField(min_length=5, max_length=15)
    cpf = BRCPFField()
    telefone = BRPhoneNumberField()

    class Meta:
        model = Funcionario

class FuncionarioEditaForm(forms.ModelForm):
    nome = forms.RegexField(u'^([a-zA-Záéíóúãeõäëïöüç]+ )+[a-zA-Záéíóúãeõäëïöüç]+$', error_message='Nome com caracteres inválidos ou incompleto.')
    telefone = BRPhoneNumberField()
    funcao = forms.ComboField(required=False)
    cpf = BRCPFField(required=False)
    rg = forms.CharField(required=False)

    class Meta:
        model = Funcionario

class FuncionarioEditaFormDadosPessoais(forms.ModelForm):
    nome = forms.CharField(required=False)
    telefone = BRPhoneNumberField()
    funcao = forms.ComboField(required=False)
    cpf = BRCPFField(required=False)
    rg = forms.CharField(required=False)
    salario = forms.DecimalField(required=False)
    periodo = forms.ChoiceField(required=False)

    class Meta:
        model = Funcionario
