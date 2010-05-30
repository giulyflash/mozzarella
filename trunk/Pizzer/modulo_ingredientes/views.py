# -*- coding: utf-8 -*-

from django.db.models import Q
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic.create_update import create_object, update_object, delete_object

from models import Ingrediente
from utils.views import lista_objetos
from views import *

@permission_required('modulo_ingredientes.pode_ver_ingredientes')
@login_required
def lista_ingredientes(request):
    nome = request.GET.get('nome')  # Obtenção dos parâmetros do request
    consulta = Q(nome__icontains=nome)
    return lista_objetos(request, [nome], Ingrediente, 'listagem_ingredientes.html', 'ingredientes', consulta)

@permission_required('modulo_ingredientes.pode_criar_ingrediente')
@login_required
def cria_ingrediente(request):
    return create_object(request, Ingrediente, 'criacao_ingrediente.html')

@permission_required('modulo_ingredientes.pode_editar_ingrediente')
@login_required
def edita_ingrediente(request, object_id):
    return update_object(request, Ingrediente, object_id, template_name='edicao_ingrediente.html')

@permission_required('modulo_ingredientes.pode_deletar_ingrediente')
@login_required
def deleta_ingrediente(request, object_id):
    return delete_object(request, Ingrediente, '/pizzer/ingredientes/', object_id, template_name='confirmacao_delecao.html', extra_context={'model': Ingrediente})