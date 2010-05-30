# -*- coding: utf-8 -*-

from django.db.models import Q
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User, Group

from models import Funcionario, FuncionarioForm, FuncionarioEditaForm
from modulo_autenticacao.models import UserCreateForm
from utils.views import lista_objetos

def lista_funcionarios(request):
    nome = request.GET.get('nome')  # Obtenção dos parâmetros do request
    consulta = Q(nome__icontains=nome)
    return lista_objetos(request, [nome], Funcionario, 'listagem_funcionarios.html', 'funcionarios', consulta)# Create your views here.

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
    return render_to_response('criacao_funcionario.html', {'form_funcionario': form_funcionario, 'form_usuario': form_usuario})

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
            funcionario.cpf = cpf
            funcionario.rg = rg
            funcionario.salario = salario
            funcionario.periodo = periodo
            funcionario.save()
            return HttpResponseRedirect('/pizzer/funcionarios/')
    else:
        form = FuncionarioEditaForm(instance=funcionario)
    return render_to_response('edicao_funcionario.html', {'form': form, 'object': funcionario})
