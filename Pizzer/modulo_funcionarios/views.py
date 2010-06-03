# -*- coding: utf-8 -*-

from django.db.models import Q
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.views.generic.create_update import create_object, update_object, delete_object

from models import Funcionario, FuncionarioForm, FuncionarioEditaForm,FuncionarioEditaFormDadosPessoais
from modulo_autenticacao.models import UserCreateForm
from utils.views import lista_objetos
from views import *

@permission_required('modulo_funcionarios.pode_ver_funcionarios')
@login_required
def lista_funcionarios(request):
    nome = request.GET.get('nome')  # Obtenção dos parâmetros do request
    consulta = Q(nome__icontains=nome)
    return lista_objetos(request, [nome], Funcionario, 'listagem_funcionarios.html', 'funcionarios', consulta)# Create your views here.

@permission_required('modulo_funcionarios.pode_criar_funcionario')
@login_required
def cria_funcionario(request):
    if request.method == 'POST':
        form_funcionario = FuncionarioForm(request.POST)
        form_usuario = UserCreateForm(request.POST)
        print form_funcionario.is_valid()
        print form_usuario.is_valid()
        if form_funcionario.is_valid() and form_usuario.is_valid():
            nome = form_funcionario.cleaned_data['nome']
            endereco = form_funcionario.cleaned_data['endereco']
            telefone = form_funcionario.cleaned_data['telefone']
            cpf = form_funcionario.cleaned_data['cpf']
            rg = form_funcionario.cleaned_data['rg']
            salario = form_funcionario.cleaned_data['salario']
            funcao = form_funcionario.cleaned_data['funcao']
            periodo = form_funcionario.cleaned_data['periodo']
            funcionario = Funcionario(nome=nome, endereco=endereco, telefone=telefone, cpf=cpf, rg=rg,
                                      salario=salario, funcao=funcao, periodo=periodo)
            username = form_usuario.cleaned_data['username']
            email = form_usuario.cleaned_data['email']
            password = form_usuario.cleaned_data['password']
            user = User.objects.create_user(username, email, password)
            user.save()
            grupo = Group.objects.get(name=funcao.lower())
            user.groups.add(grupo)
            funcionario.usuario = user
            funcionario.save()
            return HttpResponseRedirect('/pizzer/funcionarios/')
    else:
        form_funcionario = FuncionarioForm()
        form_usuario = UserCreateForm()
    return render_to_response('criacao_funcionario.html', {'form_funcionario': form_funcionario, 'form_usuario': form_usuario}, context_instance=RequestContext(request))

@permission_required('modulo_funcionarios.pode_editar_qualquer_funcionario')
@login_required
def edita_funcionario(request, object_id):
    funcionario = Funcionario.objects.get(pk=object_id)
    if request.method == 'POST':
        form = FuncionarioEditaForm(request.POST)
        if form.is_valid():
            nome = form.cleaned_data['nome']
            endereco = form.cleaned_data['endereco']
            telefone = form.cleaned_data['telefone']
            rg = form.cleaned_data['rg']
            salario = form.cleaned_data['salario']
            periodo = form.cleaned_data['periodo']
            funcionario.nome = nome
            funcionario.endereco = endereco
            funcionario.telefone = telefone
            #IMUTÁVEL funcionario.cpf = cpf
            #IMUTÁVEL funcionario.rg = rg
            funcionario.salario = salario
            funcionario.periodo = periodo
            funcionario.save()
            return HttpResponseRedirect('/pizzer/funcionarios/')
    else:
        form = FuncionarioEditaForm(instance=funcionario)
    return render_to_response('edicao_funcionario.html', {'form': form, 'object': funcionario}, context_instance=RequestContext(request))

@user_passes_test(lambda u: len(u.funcionario_set.all()) != 0)  # Precisa ser funcionário
@login_required
def edita_funcionario_dadospessoais(request, object_id):
    user = request.user
    if not user.funcionario_set.all():  # Necessário por causa do admin
        assert False
        return HttpResponseRedirect('/pizzer/usuario/login/')
    funcionario = user.funcionario_set.all()[0]
    if funcionario.id != int(object_id):
        assert False
        return HttpResponseRedirect('/pizzer/usuario/login/')
    if request.method == 'POST':
        form = FuncionarioEditaFormDadosPessoais(request.POST)
        if form.is_valid():
            nome = form.cleaned_data['nome']
            endereco = form.cleaned_data['endereco']
            telefone = form.cleaned_data['telefone']
            rg = form.cleaned_data['rg']
            salario = form.cleaned_data['salario']
            periodo = form.cleaned_data['periodo']
            #IMUTÁVEL funcionario.nome = nome
            funcionario.endereco = endereco
            funcionario.telefone = telefone
            #IMUTÁVEL funcionario.cpf = cpf
            #IMUTÁVEL funcionario.rg = rg
            #IMUTÁVEL funcionario.salario = salario
            #IMUTÁVEL funcionario.periodo = periodo
            funcionario.save()
            return HttpResponseRedirect('/pizzer/')
    else:
        form = FuncionarioEditaFormDadosPessoais(instance=funcionario)
    return render_to_response('edicao_funcionario_dadospessoais.html', {'form': form, 'object': funcionario, 'editando_dados_pessoais': True}, context_instance=RequestContext(request))

@permission_required('modulo_funcionarios.pode_deletar_funcionario')
@login_required
def deleta_funcionario(request, object_id):
    return delete_object(request, Funcionario, '/pizzer/funcionarios/', object_id, template_name='confirmacao_delecao.html', extra_context={'model': Funcionario})

@login_required
def edita_pessoa(request):  # Pode ser funcionário ou cliente
    user = request.user
    if user.funcionario_set.all():
        funcionario = user.funcionario_set.all()[0]
        redirect_url = '/pizzer/funcionario/edita/dadospessoais/%d/' % funcionario.id
    elif user.cliente_set.all():
        cliente = user.cliente_set.all()[0]
        redirect_url = '/pizzer/cliente/edita/%d/' % cliente.id
    else:
        assert False
    return HttpResponseRedirect(redirect_url)