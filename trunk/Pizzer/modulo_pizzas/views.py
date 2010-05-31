# -*- coding: utf-8 -*-

from django.views.generic import list_detail
from django.db.models import Q
from django.contrib.auth.decorators import login_required, permission_required
from django.template import RequestContext
from django.views.generic.create_update import create_object, update_object, delete_object
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect

from models import Pizza, PizzaPersonalizadaForm, Ingrediente
from utils.views import lista_objetos
from views import *

@permission_required('modulo_pizzas.pode_ver_pizzas')
@login_required
def lista_pizzas(request):
    nome = request.GET.get('nome')  # Obtenção dos parâmetros do request
    consulta = Q(nome__icontains=nome)
    return lista_objetos(request, [nome], Pizza, 'listagem_pizzas.html', 'pizzas', consulta)

@permission_required('modulo_pizzas.pode_criar_pizza')
@login_required
def cria_pizza(request):
    return create_object(request, Pizza, 'criacao_pizza.html')

@permission_required('modulo_pizzas.pode_editar_pizza')
@login_required
def edita_pizza(request, object_id):
    return update_object(request, Pizza, object_id, template_name='edicao_pizza.html')

@permission_required('modulo_pizzas.pode_deletar_pizza')
@login_required
def deleta_pizza(request, object_id):
    return delete_object(request, Pizza, '/pizzer/pizzas/', object_id, template_name='confirmacao_delecao.html', extra_context={'model': Pizza})

def cria_pizza_personalizada(request):
    cliente = request.user.cliente_set.all()[0]
    ingredientes = Ingrediente.objects.all()
    if request.method == 'POST':
        form = PizzaPersonalizadaForm(request.POST)
        if form.is_valid():
            nome = form.cleaned_data['nome']
            preco = request.POST.get('total')
            pizza = Pizza(nome=nome, preco=preco, inventor=cliente, personalizada=True)
            pizza.save()
            for ingrediente in ingredientes:
                if request.POST.get(ingrediente.nome) == 'on':
                    pizza.ingredientes.add(ingrediente)
            pizza.save()
            return HttpResponseRedirect('/pizzer/')
    else:
        form = PizzaPersonalizadaForm()
    return render_to_response('criacao_pizza_personalizada.html', {'form': form, 'ingredientes': ingredientes},
                              context_instance=RequestContext(request))

def lista_pizzas_personalizadas(request):
    cliente = request.user.cliente_set.all()[0]
    nome = request.GET.get('nome')  # Obtenção dos parâmetros do request
    consulta = Q(nome__icontains=nome) & Q(inventor=cliente);

    if request.method == 'POST':
        raise Exception('Essa view não pode ser acessada via POST')

    mensagem = ''
    if not nome:
        queryset = Pizza.objects.filter(inventor=cliente);
        if queryset:
            mensagem = 'Exibindo todos os registros.'
        else:
            mensagem = 'Não há registros a serem exibidos.'
    else:
        queryset = Pizza.objects.filter(consulta);
        if queryset:
            if len(queryset) > 1:
                mensagem = 'Foram encontrados %d resultados' % len(queryset)
            else:
                mensagem = 'Foi encontrado %d resultado' % len(queryset)
        else:
            mensagem = 'Nenhum registrado foi encontrado.'
    return list_detail.object_list(request, queryset=queryset, template_name='listagem_pizzas_personalizadas.html',
                                   template_object_name='pizzas', extra_context={'mensagem': mensagem})

