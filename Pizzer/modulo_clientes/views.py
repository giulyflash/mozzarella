# -*- coding: utf-8 -*-

from models import Cliente
from django.db.models import Q

from utils.views import lista_objetos

def lista_clientes(request):
    nome = request.GET.get('nome')  # Obtenção dos parâmetros do request
    consulta = Q(nome__icontains=nome)
    return lista_objetos(request, [nome], Cliente, 'listagem_clientes.html', 'clientes', consulta)