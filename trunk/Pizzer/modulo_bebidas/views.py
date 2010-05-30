# -*- coding: utf-8 -*-

from django.db.models import Q
from django.views.generic.create_update import create_object, update_object, delete_object
from django.contrib.auth.decorators import login_required, permission_required

from models import Bebida
from utils.views import lista_objetos
from views import *

@permission_required('modulo_bebidas.pode_ver_bebidas')
@login_required
def lista_bebidas(request):
    nome = request.GET.get('nome')  # Obtenção dos parâmetros do request
    consulta = Q(nome__icontains=nome)
    return lista_objetos(request, [nome], Bebida, 'listagem_bebidas.html', 'bebidas', consulta)

@permission_required('modulo_bebidas.pode_criar_bebida')
@login_required
def cria_bebida(request):
    return create_object(request, Bebida, 'criacao_bebida.html')

@permission_required('modulo_bebidas.pode_editar_bebida')
@login_required
def edita_bebida(request, object_id):
    return update_object(request, Bebida, object_id, template_name='edicao_bebida.html')

@permission_required('modulo_bebidas.pode_deletar_bebida')
@login_required
def deleta_bebida(request, object_id):
    return delete_object(request, Bebida, '/pizzer/bebidas/', object_id, template_name='confirmacao_delecao.html', extra_context={'model': Bebida})