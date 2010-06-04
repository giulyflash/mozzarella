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
    for username in ('dummy_personalizadas', 'dummy_mesa_1', 'dummy_mesa_2', 'dummy_mesa_3', 'dummy_mesa_4', 'dummy_mesa_5',
                     'dummy_mesa_6', 'dummy_mesa_7', 'dummy_mesa_8', 'dummy_mesa_9', 'dummy_mesa_10'):
        try:
            User.objects.get(username=username).delete()
        except Exception:
            pass

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

    return HttpResponse('Dummys criados com sucesso')

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
                           Permission.objects.get(name='Pode criar pizza personalizada'),
                           Permission.objects.get(name='Pode editar pizza personalizada'),
                           Permission.objects.get(name='Pode deletar pizza personalizada')]
    gerente.permissions = [Permission.objects.get(name='Pode criar cliente'),
                           Permission.objects.get(name='Pode ver todos os clientes'),
                           Permission.objects.get(name='Pode editar qualquer cliente'),
                           Permission.objects.get(name='Pode deletar cliente'),
                           Permission.objects.get(name='Pode ver reclamacoes'),
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
                           Permission.objects.get(name='Pode deletar ingrediente')]
    atendente.permissions = [Permission.objects.get(name='Pode criar cliente'),
                             Permission.objects.get(name='Pode ver todos os clientes'),
                             Permission.objects.get(name='Pode editar qualquer cliente'),
                             Permission.objects.get(name='Pode criar pedido'),
                             Permission.objects.get(name='Pode editar pedido'),
                             Permission.objects.get(name='Pode ver todos os pedidos'),
                             Permission.objects.get(name='Pode ver pizzas personalizadas telefone'),
                             Permission.objects.get(name='Pode ver bebidas'),
                             Permission.objects.get(name='Pode criar pizza personalizada'),
                             Permission.objects.get(name='Pode deletar pizza personalizada telefone'),
                             Permission.objects.get(name='Pode deletar pizza personalizada'),
                             Permission.objects.get(name='Pode editar pizza personalizada')]
    pizzaiolo.permissions = [Permission.objects.get(name='Pode ver todos os pedidos'),
                             Permission.objects.get(name='Pode editar pedido')]
    entregador.permissions = [Permission.objects.get(name='Pode ver pedidos a serem entregues'),
                              Permission.objects.get(name='Pode editar pedido')]
    garcom.permissions = [Permission.objects.get(name='Pode criar pedido')]

    return HttpResponse('Grupos criados com sucesso')

def cria_usuarios(request):
    for username in ('admin', 'carlos', 'vinicius', 'leonardo', 'geraldo', 'pedro', 'ana', 'eric', 'felipe', 'garcia'):
        try:
            User.objects.get(username=username).delete()
        except Exception:
            pass

    """ Criação de um superusuário (a princípio, para testes) """
    nome = 'Administrador'
    endereco = 'X'
    telefone = '11 0000-0000'
    cpf = '000000000-00'
    rg = '00000000-0'
    salario = '0.00'
    funcao = 'Gerente'
    periodo = 'T+N'
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
    nome = 'Carlos Alves de Oliveira'
    endereco = 'Rua Glicério, 194'
    telefone = '11 3207-4863'
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

    """ Criação de um cliente """
    nome = 'Vinícius Martins Lemos'
    endereco = 'Rua Doutor César Castiglioni Júnior, 186'
    telefone = '11 3858-8188'
    cliente = Cliente(nome=nome, endereco=endereco, telefone=telefone)
    username = 'vinicius'
    email = ''
    password = 'vinicius'
    user = User.objects.create_user(username, email, password)
    user.save()
    grupo = Group.objects.get(name='cliente')
    user.groups.add(grupo)
    cliente.usuario = user
    cliente.save()

    """ Criação de um cliente """
    nome = 'Leonardo Peixoto Barbosa'
    endereco = 'Avenida Lasar Segall, 390'
    telefone = '11 3981-2788'
    cliente = Cliente(nome=nome, endereco=endereco, telefone=telefone)
    username = 'leonardo'
    email = ''
    password = 'leonardo'
    user = User.objects.create_user(username, email, password)
    user.save()
    grupo = Group.objects.get(name='cliente')
    user.groups.add(grupo)
    cliente.usuario = user
    cliente.save()

    """ Criação de um gerente """
    nome = 'Geraldo Gomes Feltrin'
    endereco = 'Rua Francisco de Brito, 184'
    telefone = '11 2203-6454'
    cpf = '343837568-08'
    rg = '58943870-7'
    salario = '3500.00'
    funcao = 'Gerente'
    periodo = 'T+N'
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
    endereco = 'Rua Conselheiro Nébias, 887'
    telefone = '11 3222-5583'
    cpf = '318167518-04'
    rg = '368941546-8'
    salario = '1200.00'
    funcao = 'Pizzaiolo'
    periodo = 'T+N'
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
    nome = 'Ana Luíza Teixeira'
    endereco = 'Rua Valdemar Martins, 148'
    telefone = '11 2236-6922'
    cpf = '373152688-39'
    rg = '42864159-8'
    salario = '950.00'
    funcao = 'Atendente'
    periodo = 'T+N'
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
    nome = 'Eric Gomes Machado'
    endereco = 'Rua Agnaldo Manuel dos Santos, 270'
    telefone = '11 5084-1790'
    cpf = '368214668-74'
    rg = '45771538-8'
    salario = '700.00'
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

    """ Criação de um entregador """
    nome = 'Felipe Leon Meirelles'
    endereco = 'Rua Américo Vespucci, 1251'
    telefone = '11 2915-0040'
    cpf = '365491288-54'
    rg = '43248960-5'
    salario = '700.00'
    funcao = 'Entregador'
    periodo = 'T+N'
    funcionario = Funcionario(nome=nome, endereco=endereco, telefone=telefone, cpf=cpf, rg=rg,
                              salario=salario, funcao=funcao, periodo=periodo)
    username = 'felipe'
    email = ''
    password = 'felipe'
    user = User.objects.create_user(username, email, password)
    user.save()
    grupo = Group.objects.get(name=funcao.lower())
    user.groups.add(grupo)
    funcionario.usuario = user
    funcionario.save()

    """ Criação de um garçom """
    nome = 'Carlos Henrique Garcia'
    endereco = 'Rua Gomes Cardim, 532'
    telefone = '11 2618-3436'
    cpf = '328961028-41'
    rg = '36781357-8'
    salario = '1100.00'
    funcao = 'Garçom'
    periodo = 'N'
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
