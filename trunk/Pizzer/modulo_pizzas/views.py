# -*- coding: utf-8 -*-

from django.db.models import Q
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic.create_update import create_object, update_object, delete_object

from models import Pizza
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