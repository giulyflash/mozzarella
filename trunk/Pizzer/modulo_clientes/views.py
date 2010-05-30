# -*- coding: utf-8 -*-

from django.db.models import Q
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User, Group

from models import Cliente, ClienteForm
from modulo_autenticacao.models import UserCreateForm
from utils.views import lista_objetos

def lista_clientes(request):
    nome = request.GET.get('nome')  # Obtenção dos parâmetros do request
    consulta = Q(nome__icontains=nome)
    return lista_objetos(request, [nome], Cliente, 'listagem_clientes.html', 'clientes', consulta)

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
    return render_to_response('criacao_cliente.html', {'form_cliente': form_cliente, 'form_usuario': form_usuario})