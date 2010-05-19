# -*- coding: utf-8 -*-

from models import Cliente
from django.db.models import Q
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect

from utils.views import lista_objetos
from models import StatusItemPedido, Pedido, PedidoForm, EditaPedidoForm

def cria_pedido(request):
    if request.method == 'POST': # If the form has been submitted...
        form = PedidoForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            dono = form.cleaned_data['dono']
            status = form.cleaned_data['status']
            itens_cardapio = form.cleaned_data['itens_cardapio']
            pedido = Pedido(dono=dono, status=status)
            pedido.save()
            for item_cardapio in itens_cardapio:
                s = StatusItemPedido(item_cardapio=item_cardapio, pedido=pedido)
                s.save()
            return HttpResponseRedirect('/pizzer/pedidos/') # Redirect after POST
    else:
        form = PedidoForm() # An unbound form
    return render_to_response('criacao_pedido.html', {'form': form})

def edita_pedido(request, object_id):
    pedido = Pedido.objects.get(pk=object_id)
    if request.method == 'POST': # If the form has been submitted...
        form = EditaPedidoForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            status = form.cleaned_data['status']
            pedido.status = status
            pedido.save()
            return HttpResponseRedirect('/pizzer/pedidos/') # Redirect after POST
    else:
        form = EditaPedidoForm(instance=pedido) # An unbound form
    return render_to_response('edicao_pedido.html', {'form': form})	
    
def lista_pedidos(request):
    dono = request.GET.get('dono')  # Obtenção dos parâmetros do request
    consulta = Q(dono__nome__icontains=dono)
    return lista_objetos(request, [dono], Pedido, 'listagem_pedidos.html', 'pedidos', consulta)

