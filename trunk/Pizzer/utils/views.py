# -*- coding: utf-8 -*-

from django.views.generic import list_detail
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.contrib.auth.models import User, Permission, Group
from modulo_funcionarios.models import Funcionario
from modulo_clientes.models import Cliente

def cria_tudo(request):
    cria_grupos_usuarios(request)
    cria_usuarios(request)
    cria_clientes_dummy(request)
    return HttpResponse('Foram criados:<br/>Grupos<br/>Funcionarios<br/>Clientes<br/>Clientes dummy')

def cria_clientes_dummy(request):
    """ Criação de um cliente dummy para pizza personalizada """
    nome = 'Personalizadas'
    endereco = 'Personalizadas'
    telefone = '11 1010-1010'
    cliente = Cliente(nome=nome, endereco=endereco, telefone=telefone)
    username = 'dummy_personalizadas'
    email = ''
    password = '+h)9eyjmn_72ix%f#*@x*_r16m3'
    user = User.objects.create_user(username, email, password)
    user.save()
    grupo = Group.objects.get(name='cliente')
    user.groups.add(grupo)
    cliente.usuario = user
    cliente.save()

    """ Criação de clientes dummy para pedidos de mesas sem clientes cadastrados """
    for indice in range(1, 11):  # Mesas de 1 a 10. Sim, até 10 e não 11.
        nome = 'Mesa ' + str(indice)
        endereco = 'Mesa ' + str(indice)
        telefone = '11 1010-1010'
        cliente = Cliente(nome=nome, endereco=endereco, telefone=telefone)
        username = 'dummy_mesa_' + str(indice)
        email = ''
        password = '+h)9eyjmn_72ix%f#*@x*_r16m3'
        user = User.objects.create_user(username, email, password)
        user.save()
        grupo = Group.objects.get(name='cliente')
        user.groups.add(grupo)
        cliente.usuario = user
        cliente.save()

def cria_grupos_usuarios(request):
    for nome_grupo in ('cliente', 'gerente', 'pizzaiolo', 'atendente', 'entregador', 'garçom'):
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
                           Permission.objects.get(name='Pode criar pedido'),
                           Permission.objects.get(name='Pode criar pizza personalizada'),]
    gerente.permissions = [Permission.objects.get(name='Pode ver reclamacoes'),
                           Permission.objects.get(name='Pode resolver reclamacao'),
                           Permission.objects.get(name='Pode deletar reclamacao'),
                           Permission.objects.get(name='Pode criar funcionario'),
                           Permission.objects.get(name='Pode ver funcionarios'),
                           Permission.objects.get(name='Pode editar qualquer funcionario'),
                           Permission.objects.get(name='Pode deletar funcionario'),
                           Permission.objects.get(name='Pode ver todos os pedidos'),
                           Permission.objects.get(name='Pode editar pedido'),
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
                             Permission.objects.get(name='Pode editar pedido'),
                             Permission.objects.get(name='Pode ver todos os pedidos'),
                             Permission.objects.get(name='Pode ver pizzas'),
                             Permission.objects.get(name='Pode criar pizza personalizada'),
                             Permission.objects.get(name='Pode ver bebidas')]
    pizzaiolo.permissions = [Permission.objects.get(name='Pode ver todos os pedidos'),
                             Permission.objects.get(name='Pode editar pedido'),]
    entregador.permissions = [Permission.objects.get(name='Pode ver pedidos a serem entregues'),
                              Permission.objects.get(name='Pode editar pedido'),]
    garcom.permissions = [Permission.objects.get(name='Pode criar pedido')]
    return HttpResponse('Grupos criados com sucesso')

def cria_usuarios(request):
    for username in ('admin', 'carlos', 'geraldo', 'pedro', 'ana', 'eric', 'garcia'):
        try:
            User.objects.get(username=username).delete()
        except Exception:
            pass

    """ Criação de um superusuário (a princípio, para testes) """
    nome = 'Testador do sistema'
    endereco = 'Lugar nenhum'
    telefone = '11 1234-5678'
    cpf = '0'
    rg = '0'
    salario = '1'
    funcao = 'Gerente'
    periodo = 'N'
    funcionario = Funcionario(nome=nome, endereco=endereco, telefone=telefone, cpf=cpf, rg=rg,
                              salario=salario, funcao=funcao, periodo=periodo)
    username = 'admin'
    email = ''
    password = 'admin'
    user = User.objects.create_user(username, email, password)
    user.is_superuser = True  # superuser == tem todas as permissões
    user.save()
    grupo = Group.objects.get(name=funcao.lower())
    user.groups.add(grupo)
    funcionario.usuario = user
    funcionario.save()

    """ Criação de um cliente """
    nome = 'Carlos Alves'
    endereco = 'Av. Los pasos 51'
    telefone = '11 3951-2380'
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
    nome = 'Geraldo Gomes'
    endereco = 'Av. Dr. Arnaldo Malta'
    telefone = '11 4591-5326'
    cpf = '1'
    rg = '1'
    salario = '1'
    funcao = 'Gerente'
    periodo = 'T'
    funcionario = Funcionario(nome=nome, endereco=endereco, telefone=telefone, cpf=cpf, rg=rg,
                              salario=salario, funcao=funcao, periodo=periodo)
    username = 'geraldo'
    email = ''
    password = 'geraldo'
    user = User.objects.create_user(username, email, password)
    user.save()
    grupo = Group.objects.get(name=funcao.lower())
    user.groups.add(grupo)
    funcionario.usuario = user
    funcionario.save()

    """ Criação de um pizzaiolo """
    nome = 'Pedro Almirez'
    endereco = 'Av. Atlântica 1943'
    telefone = '11 5165-2603'
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
    endereco = 'Av. Eng. Tácio Fonseca de Souza'
    telefone = '11 7233-9158'
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
    telefone = '11 7395-8412'
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
    telefone = '11 5165-2603'
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
        return render_to_response(template_name, {'mensagem': mensagem}, context_instance=RequestContext(request))
