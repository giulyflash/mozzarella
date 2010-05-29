# -*- coding: utf-8 -*-
from django.db import models
from django.forms import ModelForm
from django import forms
from modulo_clientes.models import Cliente
from modulo_pizzas.models import ItemCardapio

STATUS_PEDIDO_CHOICES = (
    ('A', 'Registrado'),
    ('B', 'Preparo'),
    ('C', 'Espera'),
    ('D', 'Transporte'),
    ('E', 'Finalizado'),
)

class Pedido(models.Model):
    cliente = models.ForeignKey(Cliente)
    itens_cardapio = models.ManyToManyField(ItemCardapio, through='StatusItemPedido')
    status = models.CharField(max_length=10, choices=STATUS_PEDIDO_CHOICES)
    data_horario = models.DateTimeField(auto_now=True)

    def get_absolute_url():
        return '/pizzer/pedidos/'

    def status_display(self):
        return Pedido.get_status_display(self)

    def __str__(self):
        return 'Pedido' + str(self.id)

class PedidoForm(ModelForm):
    class Meta:
        model = Pedido
        exclude = ['itens_cardapio', 'status']

class StatusItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido)
    item_cardapio = models.ForeignKey(ItemCardapio)
    quantidade = models.IntegerField()
    tipo_de_item = models.IntegerField()

class EditaPedidoForm(ModelForm):
    class Meta:
        model = Pedido
        exclude = ['cliente', 'itens_cardapio']
