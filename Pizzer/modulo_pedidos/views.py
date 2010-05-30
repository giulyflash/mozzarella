# -*- coding: utf-8 -*-
from models import Cliente
from django.db.models import Q
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic.create_update import create_object, update_object, delete_object

from utils.views import lista_objetos
from views import *
from models import Cliente, ItemCardapio, StatusItemPedido, Pedido, PedidoForm, EditaPedidoForm, PagamentoForm
from modulo_pizzas.models import Pizza
from modulo_bebidas.models import Bebida

#@permission_required('modulo_pedidos.pode_criar_pedido')
#@login_required
def cria_pedido(request):
    pizzas = Pizza.objects.all()
    bebidas = Bebida.objects.all()
    if request.method == 'POST': # If the form has been submitted...
        form = PedidoForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            cliente = form.cleaned_data['cliente']
            pedido = Pedido(cliente=cliente, status='A', pagamento=0)
            pedido.save()
            vazio = True
            for pizza in pizzas:
                quantidade = request.POST.get(pizza.nome + '_qtde')
                quantidade = int(quantidade)
                if quantidade != 0:
                    s = StatusItemPedido(pedido=pedido, item_cardapio=pizza, quantidade=quantidade,
                                         tipo_de_item=1)
                    s.save()
                    pedido.pagamento += s.item_cardapio.preco * s.quantidade
                    pedido.save()
                    vazio = False
            for bebida in bebidas:
                quantidade = request.POST.get(bebida.nome + '_qtde')
                quantidade = int(quantidade)
                if quantidade != 0:
                    if bebida.quantidade - quantidade < 0:
                        pedido.delete()
                        return render_to_response('erro_estoque.html', {'bebida': bebida}, context_instance=RequestContext(request))
                    else:
                        s = StatusItemPedido(pedido=pedido, item_cardapio=bebida, quantidade=quantidade,
                                             tipo_de_item=2)
                        s.save()
                        bebida.quantidade -= quantidade
                        bebida.save()
                        pedido.pagamento += s.item_cardapio.preco * s.quantidade
                        pedido.save()
            if vazio:
                pedido.delete()
                return render_to_response('erro_vazio.html')
            return HttpResponseRedirect('/pizzer/pedido/cria/pagamento/' + str(pedido.id) + '/') # Redirect after POST
    else:
        form = PedidoForm() # An unbound form
    return render_to_response('criacao_pedido.html', {'form': form, 'bebidas': bebidas, 'pizzas': pizzas}, context_instance=RequestContext(request))

#@permission_required('modulo_pedidos.pode_criar_pedido')
#@login_required
def pagamento(request, object_id):
    pedido = Pedido.objects.get(pk=object_id)
    itens_pedidos = StatusItemPedido.objects.filter(pedido=pedido)
    total = 0
    for item_pedido in itens_pedidos:
        total += (item_pedido.item_cardapio.preco * item_pedido.quantidade)
    if request.method == 'POST': # If the form has been submitted...
        form = PagamentoForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            pagamento = form.cleaned_data['pagamento']
            if pagamento >= total:
                pedido.pagamento = pagamento
                pedido.save()
                return HttpResponseRedirect('/pizzer/pedidos/') # Redirect after POST
            else:
                pedido.delete()
                return render_to_response('erro_pagamento.html')
    else:
        form = PagamentoForm(instance=pedido)
    return render_to_response('pagamento.html', {'form':form, 'pedido':pedido, 'total': total}, context_instance=RequestContext(request))

#@permission_required('modulo_pedidos.pode_editar_pedido')
#@login_required
def edita_pedido(request, object_id):
    pedido = Pedido.objects.get(pk=object_id)
    itens_pedidos = StatusItemPedido.objects.filter(pedido=pedido)
    total = 0
    for item_pedido in itens_pedidos:
        total += (item_pedido.item_cardapio.preco * item_pedido.quantidade)
    troco = pedido.pagamento - total
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
    return render_to_response('edicao_pedido.html', {'form': form, 'bebidas': bebidas, 'pizzas': pizzas, 'pedido': pedido,
                                                     'total': total, 'troco': troco}, context_instance=RequestContext(request))

#@permission_required('modulo_pedidos.pode_ver_todos_os_pedido')
#@login_required
def lista_pedidos(request):
    cliente = request.GET.get('cliente')  # Obtenção dos parâmetros do request
    consulta = Q(cliente__nome__icontains=cliente)
    return lista_objetos(request, [cliente], Pedido, 'listagem_pedidos.html', 'pedidos', consulta)

#@permission_required('modulo_pedidos.pode_deletar_pedido')
#@login_required
def deleta_pedido(request, object_id):
    return delete_object(request, Pedido, '/pizzer/pedidos/', object_id, template_name='confirmacao_delecao.html', extra_context={'model': Pedido})

#@permission_required('modulo_pedidos.pode_criar_pedido')
#@login_required
def edita_pedido_smartphone(request, object_id):
    pedido = Pedido.objects.get(pk=object_id)
    itens_pedidos = StatusItemPedido.objects.filter(pedido=pedido)
    total = 0
    for item_pedido in itens_pedidos:
        total += (item_pedido.item_cardapio.preco * item_pedido.quantidade)
    troco = pedido.pagamento - total
    bebidas = []
    pizzas = []
    for item_pedido in itens_pedidos:
        if item_pedido.tipo_de_item == 1:
            pizzas.append(item_pedido)
        else:
            if item_pedido.tipo_de_item == 2:
                bebidas.append(item_pedido)
    if request.method == 'POST': # If the form has been submitted...
        input_status = request.POST.get('status')
        status = 'D'
        if input_status == 'Entrega Finalizada':
            status = 'E'
        else:
            if input_status == 'Problema na Entrega':
                status = 'F'
        pedido.status = status
        pedido.save()
        return HttpResponseRedirect('/pizzer/smartphone/pedidos/') # Redirect after POST
    return render_to_response('smartphone_edicao_pedido.html', {'bebidas': bebidas, 'pizzas': pizzas, 'pedido': pedido,
                                                                'troco': troco}, context_instance=RequestContext(request))

#@permission_required('modulo_pedidos.pode_ver_pedidos_a_serem_entregues')
#@login_required
def lista_pedidos_smartphone(request):
    pedidos = Pedido.objects.filter(status='D')
    return render_to_response('smartphone_listagem_pedidos.html', {'pedidos': pedidos}, context_instance=RequestContext(request))

##@login_required
def cria_pedido_pda(request):
    pizzas = Pizza.objects.all()
    bebidas = Bebida.objects.all()
    if request.method == 'POST': # If the form has been submitted...
        form = PedidoForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            cliente = form.cleaned_data['cliente']
            pedido = Pedido(cliente=cliente, status='A', pagamento=0)
            pedido.save()
            vazio = True
            for pizza in pizzas:
                quantidade = request.POST.get(pizza.nome + '_qtde')
                quantidade = int(quantidade)
                if quantidade != 0:
                    s = StatusItemPedido(pedido=pedido, item_cardapio=pizza, quantidade=quantidade,
                                         tipo_de_item=1)
                    s.save()
                    pedido.pagamento += s.item_cardapio.preco * s.quantidade
                    pedido.save()
                    vazio = False
            for bebida in bebidas:
                quantidade = request.POST.get(bebida.nome + '_qtde')
                quantidade = int(quantidade)
                if quantidade != 0:
                    if bebida.quantidade - quantidade < 0:
                        pedido.delete()
                        return render_to_response('pda_erro_estoque.html', {'bebida': bebida})
                    else:
                        s = StatusItemPedido(pedido=pedido, item_cardapio=bebida, quantidade=quantidade,
                                             tipo_de_item=2)
                        s.save()
                        bebida.quantidade -= quantidade
                        bebida.save()
                        pedido.pagamento += s.item_cardapio.preco * s.quantidade
                        pedido.save()
            if vazio:
                pedido.delete()
                return render_to_response('/pizzer/pda/pedido/cria/vazio')
            return HttpResponseRedirect('/pizzer/pedidos/') # Redirect after POST
    else:
        form = PedidoForm() # An unbound form
    return render_to_response('pda_criacao_pedido.html', {'form': form, 'bebidas': bebidas, 'pizzas': pizzas})

def edita_pedido_pda(request, object_id):
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
        input_status = request.POST.get('status')
        status = 'A'
        if input_status == 'Pedido sendo Preparado':
            status = 'B'
        else:
            if input_status == 'Pedido Pronto':
                status = 'C'
        pedido.status = status
        pedido.save()
        return HttpResponseRedirect('/pizzer/pda/pedidos/') # Redirect after POST
    return render_to_response('pda_edicao_pedido.html', {'bebidas': bebidas, 'pizzas': pizzas, 'pedido': pedido})

def lista_pedidos_pda(request):
    pedidos = Pedido.objects.filter(Q(status='A') | Q(status='B'))
    return render_to_response('pda_listagem_pedidos.html', {'pedidos': pedidos})