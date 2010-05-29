# -*- coding: utf-8 -*-

from models import Cliente
from django.db.models import Q
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect

from utils.views import lista_objetos
from models import StatusItemPedido, Pedido, PedidoForm, EditaPedidoForm
from modulo_pizzas.models import Pizza, ItemCardapio
from modulo_bebidas.models import Bebida

def cria_pedido(request):
    pizzas = Pizza.objects.all()
    bebidas = Bebida.objects.all()
    if request.method == 'POST': # If the form has been submitted...
        form = PedidoForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            cliente = form.cleaned_data['cliente']
            status = 'A'
            pedido = Pedido(cliente=cliente, status=status)
            pedido.save()
            for pizza in pizzas:
                quantidade = request.POST.get(pizza.nome + '_qtde')
                quantidade = int(quantidade)
                if quantidade != 0:
                    s = StatusItemPedido(pedido=pedido, item_cardapio=pizza, quantidade=quantidade,
                                         tipo_de_item=1)
                    s.save()
            for bebida in bebidas:
                quantidade = request.POST.get(bebida.nome + '_qtde')
                quantidade = int(quantidade)
                if quantidade != 0:
                    if bebida.quantidade - quantidade < 0:
                        pedido.delete()
                        return render_to_response('erro_estoque.html', {'bebida': bebida})
                    else:
                        s = StatusItemPedido(pedido=pedido, item_cardapio=bebida, quantidade=quantidade,
                                             tipo_de_item=2)
                        s.save()
                        bebida.quantidade -= quantidade
                        bebida.save()
            itens_pedidos = StatusItemPedido.objects.filter(pedido=pedido)
            if len(itens_pedidos) == 0:
                pedido.delete()
                return HttpResponseRedirect('/pizzer/pedido/cria/vazio')
            return HttpResponseRedirect('/pizzer/pedidos/') # Redirect after POST
    else:
        form = PedidoForm() # An unbound form
    return render_to_response('criacao_pedido.html', {'form': form, 'bebidas': bebidas, 'pizzas': pizzas})

def edita_pedido(request, object_id):
    pedido = Pedido.objects.get(pk=object_id)
    itens_pedidos = StatusItemPedido.objects.filter(pedido=pedido)
    bebidas = []
    pizzas = []
    for item_pedido in itens_pedidos:
        if item_pedido.tipo_de_item == 1:
            pizzas.append(item_pedido)
        else:
            if item_pedido.tipo_de_item == 2:
                bebidas.append(item_pedido)
    if request.method == 'POST': # If the form has been submitted...
        form = EditaPedidoForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            status = form.cleaned_data['status']
            pedido.status = status
            entregador = form.cleaned_data['entregador']
            pedido.entregador = entregador
            pedido.save()
            return HttpResponseRedirect('/pizzer/pedidos/') # Redirect after POST
    else:
        form = EditaPedidoForm(instance=pedido) # An unbound form
    return render_to_response('edicao_pedido.html', {'form': form, 'bebidas': bebidas, 'pizzas': pizzas, 'pedido': pedido})

def lista_pedidos(request):
    cliente = request.GET.get('cliente')  # Obtenção dos parâmetros do request
    consulta = Q(cliente__nome__icontains=cliente)
    return lista_objetos(request, [cliente], Pedido, 'listagem_pedidos.html', 'pedidos', consulta)

def erro_vazio(request):
    return render_to_response('erro_vazio.html')

def erro_estoque(request):
    return

