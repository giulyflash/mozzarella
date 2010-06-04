# -*- coding: utf-8 -*-

from django.db.models import Q
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.views.generic.create_update import create_object, update_object, delete_object
from django.views.generic import list_detail

from models import Cliente, ClienteForm
from modulo_autenticacao.models import UserCreateForm
from views import *

@permission_required('modulo_clientes.pode_ver_todos_os_clientes')
@login_required
def lista_clientes(request):
    nome = request.GET.get('nome')  # Obtenção dos parâmetros do request
    telefone = request.GET.get('telefone')
    consulta = Q(nome__icontains=nome) & Q(telefone__icontains=telefone) & ~Q(telefone='11 1010-1010')

    if request.method == 'POST':
        raise Exception('Essa view não pode ser acessada via POST')

    mensagem = ''
    if (not nome) and (not telefone):
        queryset = Cliente.objects.filter(~Q(telefone='11 1010-1010'))
        if queryset:
            mensagem = 'Exibindo todos os registros.'
        else:
            mensagem = 'Não há registros a serem exibidos.'
    else:
        queryset = Cliente.objects.filter(consulta);
        if queryset:
            if len(queryset) > 1:
                mensagem = 'Foram encontrados %d resultados' % len(queryset)
            else:
                mensagem = 'Foi encontrado %d resultado' % len(queryset)
        else:
            mensagem = 'Nenhum registrado foi encontrado.'
    return list_detail.object_list(request, queryset=queryset, template_name='listagem_clientes.html',
                                   template_object_name='clientes', extra_context={'mensagem': mensagem})

def snippet_lista_clientes(request):
    nome = request.GET.get('nome')
    if nome:
        clientes = Cliente.objects.filter(nome__icontains=nome)
    else:
        clientes = Cliente.objects.all()
    return render_to_response('snippet_listagem_clientes.html', {'clientes': clientes})

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
@user_passes_test(lambda u: u.has_perm('modulo_clientes.pode_editar_qualquer_cliente') or len(u.cliente_set.all()) != 0)
@login_required
def edita_cliente(request, object_id):
    user = request.user
    if user.cliente_set.all():
        cliente = user.cliente_set.all()[0]
        if not user.has_perm('modulo_funcionarios.pode_editar_qualquer_cliente') and cliente.id != int(object_id):
            return HttpResponseRedirect('/pizzer/usuario/login/')
    return update_object(request, None, object_id, template_name='edicao_cliente.html', form_class=ClienteForm)

@permission_required('modulo_clientes.pode_deletar_cliente')
@login_required
def deleta_cliente(request, object_id):
    return delete_object(request, Cliente, '/pizzer/clientes/', object_id, template_name='confirmacao_delecao.html', extra_context={'model': Cliente})