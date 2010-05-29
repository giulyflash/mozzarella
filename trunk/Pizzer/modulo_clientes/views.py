# -*- coding: utf-8 -*-

from models import Cliente
from django.db.models import Q

from utils.views import lista_objetos

def lista_clientes(request):
    nome = request.GET.get('nome')  # Obtenção dos parâmetros do request
    consulta = Q(nome__icontains=nome)
    return lista_objetos(request, [nome], Cliente, 'listagem_clientes.html', 'clientes', consulta)

def cria_cliente(request):
    if request.method == 'POST':
        form_cliente = ClienteForm(request.POST)
        form_usuario = UserCreateForm(request.POST)
        if form_cliente.is_valid() and form_usuario.is_valid():
            nome = form.cleaned_data['nome']
            endereco = form.cleaned_data['endereco']
            telefone = form.cleaned_data['telefone']
            cliente = Cliente(nome=nome, endereco=endereco, telefone=telefone)
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(username, email, password)
            user.save()
            cliente.usuario = user
            cliente.save()
            return HttpResponseRedirect('/pizzer/clientes/')
    else:
        form_cliente = ClienteForm()
        form_usuario = UserCreateForm()
    return render_to_response('criacao_cliente.html', {'form_cliente': form_cliente, 'form_usuario': form_usuario})