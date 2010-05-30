# -*- coding: utf-8 -*-

from django.views.generic import list_detail
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.contrib.auth.models import User, Permission, Group
from modulo_funcionarios.models import Funcionario
from modulo_clientes.models import Cliente

def cria_grupos_usuarios(request):
    for nome_grupo in ('cliente', 'gerente', 'pizzaiolo', 'atendente', 'motoqueiro', 'garçom'):
        try:
            Group.objects.get(name=nome_grupo).delete()
        except Exception:
            pass

    cliente = Group(name='cliente')
    cliente.save()
    gerente = Group(name='gerente')
    gerente.save()
    pizzaiolo = Group(name='pizzaiolo')
    pizzaiolo.save()
    atendente = Group(name='atendente')
    atendente.save()
    entregador = Group(name='entregador')
    entregador.save()
    garcom = Group(name='garçom')
    garcom.save()
    cliente.permissions = [Permission.objects.get(name='Pode criar reclamacao'),
                           Permission.objects.get(name='Pode criar cliente'),
                           Permission.objects.get(name='Pode criar pedido'),
                           Permission.objects.get(name='Pode criar pizza'),
                           Permission.objects.get(name='Pode ver pizzas'),
                           Permission.objects.get(name='Pode ver bebidas')]
    gerente.permissions = [Permission.objects.get(name='Pode ver reclamacoes'),
                           Permission.objects.get(name='Pode resolver reclamacao'),
                           Permission.objects.get(name='Pode deletar reclamacao'),
                           Permission.objects.get(name='Pode criar funcionario'),
                           Permission.objects.get(name='Pode ver funcionarios'),
                           Permission.objects.get(name='Pode editar qualquer funcionario'),
                           Permission.objects.get(name='Pode deletar funcionario'),
                           Permission.objects.get(name='Pode ver todos os pedidos'),
                           Permission.objects.get(name='Pode criar pizza'),
                           Permission.objects.get(name='Pode ver pizzas'),
                           Permission.objects.get(name='Pode editar pizza'),
                           Permission.objects.get(name='Pode deletar pizza'),
                           Permission.objects.get(name='Pode criar bebida'),
                           Permission.objects.get(name='Pode ver bebidas'),
                           Permission.objects.get(name='Pode editar bebida'),
                           Permission.objects.get(name='Pode deletar bebida'),
                           Permission.objects.get(name='Pode criar ingrediente'),
                           Permission.objects.get(name='Pode ver ingredientes'),
                           Permission.objects.get(name='Pode editar ingrediente'),
                           Permission.objects.get(name='Pode deletar ingrediente'),]
    atendente.permissions = [Permission.objects.get(name='Pode criar cliente'),
                             Permission.objects.get(name='Pode ver todos os clientes'),
                             Permission.objects.get(name='Pode editar qualquer cliente'),
                             Permission.objects.get(name='Pode criar pedido'),
                             Permission.objects.get(name='Pode ver todos os pedidos'),
                             Permission.objects.get(name='Pode criar pizza'),
                             Permission.objects.get(name='Pode ver pizzas'),
                             Permission.objects.get(name='Pode ver bebidas')]
    pizzaiolo.permissions = [Permission.objects.get(name='Pode ver todos os pedidos'),
                             Permission.objects.get(name='Pode ver ingredientes'),]
    entregador.permissions = [Permission.objects.get(name='Pode ver pedidos a serem entregues'),
                              Permission.objects.get(name='Pode ver detalhes de cliente com pedido'),]
    garcom.permissions = [Permission.objects.get(name='Pode criar pedido'),
                          Permission.objects.get(name='Pode ver todos os pedidos'),]
    return HttpResponse('Grupos criados com sucesso')

def cria_usuarios(request):
    for username in ('admin', 'carlos', 'bob', 'pedro', 'ana', 'eric', 'garcia'):
        try:
            User.objects.get(username=username).delete()
        except Exception:
            pass

    """ Criação de um superusuário (a princípio, para testes) """
    username = 'admin'
    email = ''
    password = 'admin'
    user = User.objects.create_user(username, email, password)
    user.is_superuser = True  # superuser == tem todas as permissões
    user.save()

    """ Criação de um cliente """
    nome = 'Carlos Alves'
    endereco = 'Av. Los pasos 51'
    telefone = '3951-2380'
    cliente = Cliente(nome=nome, endereco=endereco, telefone=telefone)
    username = 'carlos'
    email = ''
    password = 'carlos'
    user = User.objects.create_user(username, email, password)
    user.save()
    grupo = Group.objects.get(name='cliente')
    user.groups.add(grupo)
    cliente.usuario = user
    cliente.save()

    """ Criação de um gerente """
    nome = 'Bob, o gerente'
    endereco = 'Reijavic, Islândia'
    telefone = '33 10 4591-5326'
    cpf = '1'
    rg = '1'
    salario = '1'
    funcao = 'Gerente'
    periodo = 'T'
    funcionario = Funcionario(nome=nome, endereco=endereco, telefone=telefone, cpf=cpf, rg=rg,
                              salario=salario, funcao=funcao, periodo=periodo)
    username = 'bob'
    email = ''
    password = 'bob'
    user = User.objects.create_user(username, email, password)
    user.save()
    grupo = Group.objects.get(name=funcao.lower())
    user.groups.add(grupo)
    funcionario.usuario = user
    funcionario.save()

    """ Criação de um pizzaiolo """
    nome = 'Pedro Almirez'
    endereco = 'Av. Atlântica 1943'
    telefone = '5165-2603'
    cpf = '2'
    rg = '2'
    salario = '1'
    funcao = 'Pizzaiolo'
    periodo = 'T'
    funcionario = Funcionario(nome=nome, endereco=endereco, telefone=telefone, cpf=cpf, rg=rg,
                              salario=salario, funcao=funcao, periodo=periodo)
    username = 'pedro'
    email = ''
    password = 'pedro'
    user = User.objects.create_user(username, email, password)
    user.save()
    grupo = Group.objects.get(name=funcao.lower())
    user.groups.add(grupo)
    funcionario.usuario = user
    funcionario.save()

    """ Criação de um atendente """
    nome = 'Ana Luíza'
    endereco = 'Av. Eng. Bob'
    telefone = '7233-9158'
    cpf = '3'
    rg = '3'
    salario = '1'
    funcao = 'Atendente'
    periodo = 'T'
    funcionario = Funcionario(nome=nome, endereco=endereco, telefone=telefone, cpf=cpf, rg=rg,
                              salario=salario, funcao=funcao, periodo=periodo)
    username = 'ana'
    email = ''
    password = 'ana'
    user = User.objects.create_user(username, email, password)
    user.save()
    grupo = Group.objects.get(name=funcao.lower())
    user.groups.add(grupo)
    funcionario.usuario = user
    funcionario.save()

    """ Criação de um entregador """
    nome = 'Eric Gomes'
    endereco = 'R. Estados Unidos 5501'
    telefone = '7395-8412'
    cpf = '4'
    rg = '4'
    salario = '1'
    funcao = 'Entregador'
    periodo = 'T'
    funcionario = Funcionario(nome=nome, endereco=endereco, telefone=telefone, cpf=cpf, rg=rg,
                              salario=salario, funcao=funcao, periodo=periodo)
    username = 'eric'
    email = ''
    password = 'eric'
    user = User.objects.create_user(username, email, password)
    user.save()
    grupo = Group.objects.get(name=funcao.lower())
    user.groups.add(grupo)
    funcionario.usuario = user
    funcionario.save()

    """ Criação de um garçom """
    nome = 'Garcia da Silva Sauro'
    endereco = 'R. Dr. Aluísio Fonseca Cruz del Aroyo'
    telefone = '5165-2603'
    cpf = '5'
    rg = '5'
    salario = '2'
    funcao = 'Garçom'
    periodo = 'T'
    funcionario = Funcionario(nome=nome, endereco=endereco, telefone=telefone, cpf=cpf, rg=rg,
                              salario=salario, funcao=funcao, periodo=periodo)
    username = 'garcia'
    email = ''
    password = 'garcia'
    user = User.objects.create_user(username, email, password)
    user.save()
    grupo = Group.objects.get(name=funcao.lower())
    user.groups.add(grupo)
    funcionario.usuario = user
    funcionario.save()


    return HttpResponse('Clientes e funcionarios criados com sucesso')

def lista_objetos(request, parametros, model, template_name, template_object_name, consulta, universo=None):
    mensagem = ''
    nenhum_param_enviado = True
    if request.method == 'POST':
        raise Exception('Essa view não pode ser acessada via POST')
    for parametro in parametros:
        if parametro:  # Se qualquer parâmetro tiver sido usado:
            nenhum_param_enviado = False
            break
    if nenhum_param_enviado:
        if universo:
            queryset = model.objects.filter(universo);
        else:
            queryset = model.objects.all();
        if queryset:
            mensagem = 'Exibindo todos os registros.'
        else:
            mensagem = 'Não há registros a serem exibidos.'
    else:
        if universo:
            queryset = model.objects.filter(consulta & universo);
        else:
            queryset = model.objects.filter(consulta);
        if queryset:
            if len(queryset) > 1:
                mensagem = 'Foram encontrados %d resultados' % len(queryset)
            else:
                mensagem = 'Foi encontrado %d resultado' % len(queryset)
        else:
            mensagem = 'Nenhum registrado foi encontrado.'
    return list_detail.object_list(request,
    queryset=queryset,
    template_name=template_name,
    template_object_name=template_object_name, extra_context={'mensagem': mensagem})



    if not queryset:
        mensagem = 'Não há registros a serem exibidos.'
    else:
        mensagem = 'Exibindo todos os registros.'
    if queryset:
        return list_detail.object_list(request,
            queryset=queryset,
            template_name=template_name,
            template_object_name=template_object_name, extra_context={'mensagem': mensagem})
    else:
        return render_to_response(template_name, {'mensagem': mensagem})# Create your views here.
