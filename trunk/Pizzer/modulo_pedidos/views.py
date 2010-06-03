# -*- coding: utf-8 -*-
from models import Cliente
from django.db.models import Q
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.views.generic.create_update import create_object, update_object, delete_object

from utils.views import lista_objetos
from views import *
from models import Cliente, ItemCardapio, StatusItemPedido, Pedido, PedidoForm, PedidoFormPDA, PedidoFormParaCliente, EditaPedidoForm
from modulo_pizzas.models import Pizza, ItemCardapio
from modulo_bebidas.models import Bebida

@permission_required('modulo_pedidos.pode_criar_pedido')
@login_required
def cria_pedido(request):
    user = request.user
    if user.groups.all():
        grupo = user.groups.all()[0].name
        if grupo == 'cliente':
            cliente = user.cliente_set.all()[0]
            pizzas = Pizza.objects.filter(Q(personalizada=False) | Q(inventor=cliente))
        else:
            pizzas = Pizza.objects.filter(personalizada=False)
    elif user.is_authenticated():
        grupo = 'admin'
        pizzas = Pizza.objects.filter(personalizada=False)
    else:
        grupo = u'anônimo'
        pizzas = Pizza.objects.filter(personalizada=False)
    bebidas = Bebida.objects.all()
    if request.method == 'POST':
        if grupo == 'cliente':
            form = PedidoFormParaCliente(request.POST)
        else:
            form = PedidoForm(request.POST)
        if form.is_valid():
            if grupo != 'cliente':
                cliente = form.cleaned_data['cliente']
            pagamento = form.cleaned_data['pagamento']
            pedido = Pedido(cliente=cliente, status='A', pagamento=pagamento)
            pedido.save()
            total = 0
            vazio = True
            for pizza in pizzas:
                quantidade = request.POST.get(pizza.nome + '_qtde')
                quantidade = int(quantidade)
                if quantidade != 0:
                    s = StatusItemPedido(pedido=pedido, item_cardapio=pizza, quantidade=quantidade,
                                         tipo_de_item=1)
                    s.save()
                    total += s.item_cardapio.preco * s.quantidade
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
                        total += s.item_cardapio.preco * s.quantidade
            if vazio or (pagamento < total):
                pedido.delete()
            return HttpResponseRedirect('/pizzer/') # Redirect after POST
    else:
        if grupo == 'cliente':
            form = PedidoFormParaCliente(initial={'pagamento': '0.00'})
        else:
            form = PedidoForm({'pagamento': '0.00'})
    return render_to_response('criacao_pedido.html', {'form': form, 'bebidas': bebidas, 'pizzas': pizzas}, context_instance=RequestContext(request))

@permission_required('modulo_pedidos.pode_editar_pedido')
@login_required
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

@permission_required('modulo_pedidos.pode_ver_todos_os_pedidos')
@login_required
def lista_pedidos(request):
    cliente = request.GET.get('cliente')  # Obtenção dos parâmetros do request
    consulta = Q(cliente__nome__icontains=cliente)
    return lista_objetos(request, [cliente], Pedido, 'listagem_pedidos.html', 'pedidos', consulta)

def cancela_pedido(request, object_id):
    pedido = Pedido.objects.get(pk=object_id)
    itens_pedidos = StatusItemPedido.objects.filter(pedido=pedido)
    bebidas = Bebida.objects.all()
    if request.method == 'POST': # If the form has been submitted...
        for item_pedido in itens_pedidos:
            if item_pedido.tipo_de_item == 2:
                for bebida in bebidas:
                    if item_pedido.item_cardapio.nome == bebida.nome:
                        bebida.quantidade += item_pedido.quantidade
                        bebida.save()
                        break
        pedido.delete()
        return HttpResponseRedirect('/pizzer/pedidos/') # Redirect after POST
    return render_to_response('cancelamento_pedido.html', {'pedido': pedido})

@permission_required('modulo_pedidos.pode_deletar_pedido')
@login_required
def deleta_pedido(request, object_id):
    return delete_object(request, Pedido, '/pizzer/pedidos/', object_id, template_name='confirmacao_delecao.html', extra_context={'model': Pedido})

@permission_required('modulo_pedidos.pode_editar_pedido')
@login_required
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

@permission_required('modulo_pedidos.pode_ver_pedidos_a_serem_entregues')
@login_required
def lista_pedidos_smartphone(request):
    try:
        entregador = request.user.funcionario_set.all()[0]
    except IndexError:
        return HttpResponse(u'Apenas um entregador pode acessar essa área')
    pedidos = Pedido.objects.filter(status='D', entregador=entregador)
    return render_to_response('smartphone_listagem_pedidos.html', {'pedidos': pedidos}, context_instance=RequestContext(request))

@permission_required('modulo_pedidos.pode_criar_pedido')
@login_required
def cria_pedido_pda(request):
    pizzas = Pizza.objects.filter(personalizada=False)
    bebidas = Bebida.objects.all()
    if request.method == 'POST': # If the form has been submitted...
        form = PedidoFormPDA(request.POST) # A form bound to the POST data
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
                return render_to_response('pda_erro_vazio.html', context_instance=RequestContext(request))
            return HttpResponseRedirect('/pizzer/') # Redirect after POST
    else:
        form = PedidoFormPDA() # An unbound form
    return render_to_response('pda_criacao_pedido.html', {'form': form, 'bebidas': bebidas, 'pizzas': pizzas}, context_instance=RequestContext(request))

@permission_required('modulo_pedidos.pode_editar_pedido')
@login_required
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
    return render_to_response('pda_edicao_pedido.html', {'bebidas': bebidas, 'pizzas': pizzas, 'pedido': pedido},
                              context_instance=RequestContext(request))

@permission_required('modulo_pedidos.pode_ver_todos_os_pedidos')
@login_required
def lista_pedidos_pda(request):
    pedidos = Pedido.objects.filter(Q(status='A') | Q(status='B'))
    return render_to_response('pda_listagem_pedidos.html', {'pedidos': pedidos}, context_instance=RequestContext(request))

@user_passes_test(lambda u: u.groups.filter(name='cliente').count() != 0)
@login_required
def lista_pedidos_cliente(request):
    cliente = request.user.cliente_set.all()[0]
    pedidos = Pedido.objects.filter(cliente=cliente)
    return render_to_response('listagem_pedidos_cliente.html', {'pedidos': pedidos}, context_instance=RequestContext(request))