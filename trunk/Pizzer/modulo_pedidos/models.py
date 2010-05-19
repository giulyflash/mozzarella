# -*- coding: utf-8 -*-
from django.db import models
from django.forms import ModelForm
from django import forms
from modulo_clientes.models import Cliente
from modulo_pizzas.models import ItemCardapio

STATUS_PEDIDO_CHOICES = (  # e.g. todos itens atendidos
    ('NA', 'Todos itens prontos'),
    ('SE', 'Sendo entregue pelo motoqueiro'),
    ('E', 'Entrada'),
    ('NPE', 'Nao Pode ser entregue'),
)

STATUS_ITEM_PEDIDO_CHOICES = (  # e.g. pizza pronta, bebida entregue
    ('NA', 'Nao atendido'),
    ('EP', 'Em preparo'),
    ('P', 'Pronto'),
)

class Pedido(models.Model):
    dono = models.ForeignKey(Cliente)
    itens_cardapio = models.ManyToManyField(ItemCardapio, through='StatusItemPedido')
    status = models.CharField(max_length=10, choices=STATUS_PEDIDO_CHOICES)
    data_horario = models.DateTimeField(auto_now=True)
    
    def get_absolute_url():
        return '/pizzer/pedidos/'

    def status_display(self):
        return Pedido.get_status_display(self)
        
class PedidoForm(ModelForm):
    class Meta:
        model = Pedido

class StatusItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido)
    item_cardapio = models.ForeignKey(ItemCardapio)
    status = models.CharField(max_length=3, choices=STATUS_ITEM_PEDIDO_CHOICES)
    
class EditaPedidoForm(ModelForm):
    class Meta:
        model = Pedido

