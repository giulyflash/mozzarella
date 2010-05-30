# -*- coding: utf-8 -*-

from django.db.models import Q
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.views.generic.create_update import create_object, update_object, delete_object

from models import Cliente, ClienteForm
from modulo_autenticacao.models import UserCreateForm
from utils.views import lista_objetos
from views import *

@permission_required('modulo_clientes.pode_ver_todos_os_clientes')
@login_required
def lista_clientes(request):
    nome = request.GET.get('nome')  # Obtenção dos parâmetros do request
    consulta = Q(nome__icontains=nome)
    return lista_objetos(request, [nome], Cliente, 'listagem_clientes.html', 'clientes', consulta)

# Qualquer um pode cadastrar-se, logo, não há restrição por login
def cria_cliente(request):
    if request.method == 'POST':
        form_cliente = ClienteForm(request.POST)
        form_usuario = UserCreateForm(request.POST)
        print form_cliente.is_valid()
        print form_usuario.is_valid()
        if form_cliente.is_valid() and form_usuario.is_valid():
            nome = form_cliente.cleaned_data['nome']
            endereco = form_cliente.cleaned_data['endereco']
            telefone = form_cliente.cleaned_data['telefone']
            cliente = Cliente(nome=nome, endereco=endereco, telefone=telefone)
            username = form_usuario.cleaned_data['username']
            email = form_usuario.cleaned_data['email']
            password = form_usuario.cleaned_data['password']
            user = User.objects.create_user(username, email, password)
            user.save()
            grupo_cliente = Group.objects.get(name='cliente')
            user.groups.add(grupo_cliente)
            cliente.usuario = user
            cliente.save()
            return HttpResponseRedirect('/pizzer/clientes/')
    else:
        form_cliente = ClienteForm()
        form_usuario = UserCreateForm()
    return render_to_response('criacao_cliente.html', {'form_cliente': form_cliente, 'form_usuario': form_usuario}, context_instance=RequestContext(request))

#  Pode editar cliente se tiver permissão para editar qualquer cliente, ou se forem seus próprios dados
@user_passes_test(lambda u: u.has_perm('modulo_clientes.pode_editar_qualquer_cliente') or u.cliente_set.all())
@login_required
def edita_cliente(request, object_id):
    user = request.user
    cliente = user.cliente_set.all()[0]
    if not user.has_perm('modulo_funcionarios.pode_editar_qualquer_cliente') and cliente.id != int(object_id):
        return HttpResponseRedirect('/pizzer/usuario/login/')
    return update_object(request, Cliente, object_id, template_name='edicao_cliente.html')

@permission_required('modulo_clientes.pode_deletar_cliente')
@login_required
def deleta_cliente(request, object_id):
    return delete_object(request, Cliente, '/pizzer/clientes/', object_id, template_name='confirmacao_delecao.html', extra_context={'model': Cliente})