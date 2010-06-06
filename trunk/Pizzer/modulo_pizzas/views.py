# -*- coding: utf-8 -*-

from django.views.generic import list_detail
from django.db.models import Q
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.template import RequestContext
from django.views.generic.create_update import create_object, update_object, delete_object
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect

from models import Pizza, PizzaPersonalizadaForm, Ingrediente, Cliente
from utils.views import lista_objetos
from views import *

@permission_required('modulo_pizzas.pode_ver_pizzas')
@login_required
def lista_pizzas(request):
    nome = request.GET.get('nome')  # Obtenção dos parâmetros do request
    consulta = Q(nome__icontains=nome)
    universo = Q(inventor__isnull=True)
    return lista_objetos(request, [nome], Pizza, 'listagem_pizzas.html', 'pizzas', consulta, universo)

@permission_required('modulo_pizzas.pode_criar_pizza')
@login_required
def cria_pizza(request):
    return create_object(request, Pizza, 'criacao_pizza.html', post_save_redirect='/pizzer/pizzas/')

@user_passes_test(lambda u: u.has_perm('modulo_pizzas.pode_editar_pizza') or len(u.cliente_set.all()) != 0)
@login_required
def edita_pizza(request, object_id):
    user = request.user
    if user.cliente_set.all():
       cliente = user.cliente_set.all()[0]
       pizza = Pizza.objects.get(id=object_id)
       if pizza.inventor != cliente:
           return HttpResponseRedirect('/pizzer/usuario/login/')
    return update_object(request, Pizza, object_id, template_name='edicao_pizza.html')

@permission_required('modulo_pizzas.pode_deletar_pizza')
@login_required
def deleta_pizza(request, object_id):
    return delete_object(request, Pizza, '/pizzer/pizzas/', object_id, template_name='confirmacao_delecao.html', extra_context={'model': Pizza})

@user_passes_test(lambda u: len(u.groups.filter(name='cliente')) != 0 or len(u.groups.filter(name='atendente')) != 0)
@login_required
def cria_pizza_personalizada(request):
    cliente_criando_pessoalmente = len(request.user.cliente_set.all()) != 0
    if cliente_criando_pessoalmente:
        cliente = request.user.cliente_set.all()[0]
    else:
        cliente = Cliente.objects.get(nome='Personalizadas')
    ingredientes = Ingrediente.objects.all()
    if request.method == 'POST':
        form = PizzaPersonalizadaForm(request.POST)
        if form.is_valid():
            nome = form.cleaned_data['nome']
            preco = 15
            pizza = Pizza(nome=nome, preco=preco, inventor=cliente, personalizada=True)
            pizza.save()
            for ingrediente in ingredientes:
                if request.POST.get(ingrediente.nome) == 'on':
                    pizza.ingredientes.add(ingrediente)
                    pizza.preco += ingrediente.preco
            pizza.save()
            if cliente_criando_pessoalmente:
                return HttpResponseRedirect('/pizzer/pizzas/personalizadas')
            return HttpResponseRedirect('/pizzer/pizzas/personalizadas/telefone')
    else:
        form = PizzaPersonalizadaForm()
    return render_to_response('criacao_pizza_personalizada.html', {'form': form, 'ingredientes': ingredientes},
                              context_instance=RequestContext(request))

@user_passes_test(lambda u: u.groups.filter(name='cliente').count() != 0)
@login_required
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

@permission_required('modulo_pizzas.pode_editar_pizza_personalizada')
@login_required
def edita_pizza_personalizada(request, object_id):
    pizza = Pizza.objects.get(pk=object_id)
    inventor = pizza.inventor
    ingredientes = Ingrediente.objects.all()
    if request.method == 'POST':
        pizza.delete()
        form = PizzaPersonalizadaForm(request.POST)
        if form.is_valid():
            nome = form.cleaned_data['nome']
            pizza = Pizza(nome=nome, inventor=inventor, preco=15, personalizada=True)
            pizza.save()
            for ingrediente in ingredientes:
                if request.POST.get(ingrediente.nome) == 'on':
                    pizza.ingredientes.add(ingrediente)
                    pizza.preco += ingrediente.preco
            pizza.save()
            return HttpResponseRedirect('/pizzer/')
    else:
        ingredientes1 = pizza.ingredientes.all()
        ingredientes2 = ingredientes
        for ingrediente in ingredientes1:
            ingredientes2 = ingredientes2.exclude(nome=ingrediente.nome)
        form = PizzaPersonalizadaForm(instance=pizza)
    return render_to_response('edicao_pizza_personalizada.html', {'form': form, 'pizza': pizza, 'ingredientes': ingredientes,
                                                                  'ingredientes1': ingredientes1, 'ingredientes2': ingredientes2},
                                                                  context_instance=RequestContext(request))
@permission_required('modulo_pizzas.pode_deletar_pizza_personalizada')
@login_required
def deleta_pizza_personalizada(request, object_id):
    cliente_usuario = len(request.user.cliente_set.all()) != 0
    if cliente_usuario:
        return delete_object(request, Pizza, '/pizzer/pizzas/personalizadas/', object_id, template_name='confirmacao_delecao.html', extra_context={'model': Pizza})
    return delete_object(request, Pizza, '/pizzer/pizzas/personalizadas/telefone/', object_id, template_name='confirmacao_delecao.html', extra_context={'model': Pizza})

@permission_required('modulo_pizzas.pode_ver_pizzas_personalizadas_telefone')
@login_required
def lista_pizzas_personalizadas_telefone(request):
    nome = request.GET.get('nome')  # Obtenção dos parâmetros do request
    consulta = Q(nome__icontains=nome) & Q(inventor__nome='Personalizadas');

    if request.method == 'POST':
        raise Exception('Essa view não pode ser acessada via POST')

    mensagem = ''
    if not nome:
        queryset = Pizza.objects.filter(inventor__nome='Personalizadas');
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
    return list_detail.object_list(request, queryset=queryset, template_name='listagem_pizzas_personalizadas_telefone.html',
                                   template_object_name='pizzas', extra_context={'mensagem': mensagem})

@permission_required('modulo_pizzas.pode_deletar_pizza_personalizada_telefone')
@login_required
def deleta_pizzas_personalizadas_telefone(request):
    if request.method == 'POST':
        pizzas = Pizza.objects.filter(inventor__nome='Personalizadas')
        for pizza in pizzas:
            pizza.delete()
        return HttpResponseRedirect('/pizzer/pizzas/personalizadas/telefone/')
    return render_to_response('confirmacao_delecao_personalizadas.html', context_instance=RequestContext(request))


