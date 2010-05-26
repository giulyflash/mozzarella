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
    itens_cardapio = ItemCardapio.objects.all()
    if request.method == 'POST': # If the form has been submitted...
        form = PedidoForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            dono = form.cleaned_data['dono']
            status = form.cleaned_data['status']
            pedido = Pedido(dono=dono, status=status)
            pedido.save()
            for item_cardapio in itens_cardapio:
                quantidade = request.POST.get(item_cardapio.nome + '_qtde')
                quantidade = int(quantidade)
                if quantidade != 0:
                    s = StatusItemPedido(pedido=pedido, item_cardapio=item_cardapio, quantidade=quantidade)
                    s.save()
            return HttpResponseRedirect('/pizzer/pedidos/') # Redirect after POST
    else:
        form = PedidoForm() # An unbound form
    return render_to_response('criacao_pedido.html', {'form': form, 'bebidas': bebidas, 'pizzas': pizzas})

def edita_pedido(request, object_id):
    pedido = Pedido.objects.get(pk=object_id)
    bebidas = StatusItemPedido.objects.filter(pedido=pedido)
    if request.method == 'POST': # If the form has been submitted...
        form = EditaPedidoForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            status = form.cleaned_data['status']
            pedido.status = status
            pedido.save()
            return HttpResponseRedirect('/pizzer/pedidos/') # Redirect after POST
    else:
        form = EditaPedidoForm(instance=pedido) # An unbound form
    return render_to_response('edicao_pedido.html', {'form': form, 'bebidas': bebidas, 'pedido': pedido})	
    
def lista_pedidos(request):
    dono = request.GET.get('dono')  # Obtenção dos parâmetros do request
    consulta = Q(dono__nome__icontains=dono)
    return lista_objetos(request, [dono], Pedido, 'listagem_pedidos.html', 'pedidos', consulta)

