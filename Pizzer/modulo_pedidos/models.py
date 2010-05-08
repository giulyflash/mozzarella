# -*- coding: utf-8 -*-
from django.db import models
from django.forms import ModelForm

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
    itens_cardapio = ManyToManyKey(ItemCardapio, through=StatusItemPedido)
    status = models.CharField(max_length=10, choices=STATUS_PEDIDO_CHOICES)
    data_horario = models.DateTimeField(auto_now=True)

class StatusItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido)
    item_cardapio = models.ForeignKey(ItemCardapio)
    status = models.CharField(choices=STATUS_ITEM_PEDIDO_CHOICES)


