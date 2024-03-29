# -*- coding: utf-8 -*-

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q
from utils.views import lista_objetos
from models import UserCreateForm, UserEditForm, UserChangePassForm

@login_required
def index(request):
    if request.user.groups.all():
        group = request.user.groups.all()[0].name
        if  group == 'pizzaiolo':
            return HttpResponseRedirect('/pizzer/pda/pedidos/')
        elif group == 'entregador':
            return HttpResponseRedirect('/pizzer/smartphone/pedidos/')
        elif group == u'garçom':
            return HttpResponseRedirect('/pizzer/pda/pedido/cria/')
    return render_to_response('index.html', context_instance=RequestContext(request))

def faz_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/pizzer/')
            else:
                return render_to_response('formulario_login.html', {'erro': 'Esse usuario foi desativado.'}, context_instance=RequestContext(request))
        else:
            return render_to_response('formulario_login.html', {'erro': 'Nome de usuario ou senha incorretos.'}, context_instance=RequestContext(request))
    else:
        return render_to_response('formulario_login.html', context_instance=RequestContext(request))

from django.contrib.auth import logout

def faz_logout(request):
    logout(request)
    return HttpResponseRedirect('/pizzer/usuario/login/')


def lista_usuarios(request):
    username = request.GET.get('username')  # Obten��o dos par�metros do request
    consulta = Q(nome__icontains=username)
    return lista_objetos(request, [username], User, 'listagem_usuarios.html', 'usuarios', consulta)

def cria_usuario(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(username, email, password)
            user.save()
            return HttpResponseRedirect('/pizzer/usuarios/')
    else:
        form = UserCreateForm()
    return render_to_response('criacao_usuario.html', {'form': form}, context_instance=RequestContext(request))

def edita_usuario(request, object_id):
    user = User.objects.get(pk=object_id)
    if request.method == 'POST':
        form = UserEditForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user.username = username
            user.email = email
            user.set_password(password)
            user.save()
            return HttpResponseRedirect('/pizzer/usuarios/')
    else:
        form = UserEditForm(instance=user)
    return render_to_response('edita_usuario.html', {'form': form}, context_instance=RequestContext(request))

def muda_senha_cliente(request, object_id):
    user = User.objects.get(pk=object_id)
    cliente = user.cliente_set.all()[0]
    if request.method == 'POST':
        form = UserChangePassForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()
            return HttpResponseRedirect('/pizzer/cliente/edita/%s/' % cliente.id)
    else:
        form = UserChangePassForm()
    return render_to_response('mudanca_senha.html', {'form': form, 'cliente': cliente, 'pessoa': 'cliente'}, context_instance=RequestContext(request))

def muda_senha_funcionario(request, object_id):
    user = User.objects.get(pk=object_id)
    funcionario = user.funcionario_set.all()[0]
    if request.method == 'POST':
        form = UserChangePassForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()
            return HttpResponseRedirect('/pizzer/funcionario/edita/dadospessoais/%s/' % funcionario.id)
    else:
        form = UserChangePassForm()
    return render_to_response('mudanca_senha.html', {'form': form, 'funcionario': funcionario, 'pessoa': 'funcionario'}, context_instance=RequestContext(request))