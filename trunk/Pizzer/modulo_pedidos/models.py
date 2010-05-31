# -*- coding: utf-8 -*-
from django.db import models
from django.forms import ModelForm
from django import forms

from modulo_clientes.models import Cliente
from modulo_pizzas.models import ItemCardapio, Pizza
from modulo_bebidas.models import Bebida
from modulo_funcionarios.models import Funcionario

STATUS_PEDIDO_CHOICES = (
    ('A', 'Registrado'),
    ('B', 'Em Preparo'),
    ('C', 'Em Espera'),
    ('D', 'Em Transporte'),
    ('E', 'Finalizado'),
    ('F', 'Não Pôde Ser Entregue')
)

class Pedido(models.Model):
    cliente = models.ForeignKey(Cliente)
    itens_cardapio = models.ManyToManyField(ItemCardapio, through='StatusItemPedido')
    status = models.CharField(max_length=10, choices=STATUS_PEDIDO_CHOICES)
    entregador = models.ForeignKey(Funcionario, blank=True, null=True)
    data_horario = models.DateTimeField(auto_now_add=True)
    pagamento = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        permissions = (
           ('pode_criar_pedido', 'Pode criar pedido'),
            ('pode_ver_todos_os_pedidos', 'Pode ver todos os pedidos'),
            ('pode_ver_pedidos_a_serem_entregues', 'Pode ver pedidos a serem entregues'),
            ('pode_editar_pedido', 'Pode editar pedido'),
            ('pode_deletar_pedido', 'Pode deletar pedido'),
        )

    def get_absolute_url():
        return '/pizzer/pedidos/'

    def status_display(self):
        return Pedido.get_status_display(self)

    def get_itens_pedido(self):
        return StatusItemPedido.objects.filter(pedido=self)

    def get_pizzas(self):
        itens_pedido = []
        for pizza in Pizza.objects.all():
            if pizza.statusitempedido_set.filter(pedido=self):
                itens_pedido.append(pizza.statusitempedido_set.get(pedido=self))
        return itens_pedido

    def get_bebidas(self):
        itens_pedido = []
        for bebida in Bebida.objects.all():
            if bebida.statusitempedido_set.filter(pedido=self):
                itens_pedido.append(bebida.statusitempedido_set.get(pedido=self))
        return itens_pedido

    def __str__(self):
        return 'Pedido' + str(self.id)

class StatusItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido)
    item_cardapio = models.ForeignKey(ItemCardapio)
    quantidade = models.IntegerField()
    tipo_de_item = models.IntegerField()

class PedidoForm(ModelForm):
    class Meta:
        model = Pedido
        exclude = ['itens_cardapio', 'status', 'entregador']

class PedidoFormParaCliente(ModelForm):
    cliente = forms.ComboField(required=False)
    class Meta:
        model = Pedido
        exclude = ['itens_cardapio', 'status', 'entregador']

class EditaPedidoForm(ModelForm):
    entregador = forms.ModelChoiceField(queryset=Funcionario.objects.filter(funcao='Entregador'), required=False)

    class Meta:
        model = Pedido
        exclude = ['cliente', 'itens_cardapio', 'pagamento']

