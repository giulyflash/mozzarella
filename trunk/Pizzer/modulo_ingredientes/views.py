# -*- coding: utf-8 -*-

from django.db.models import Q

from models import Ingrediente
from utils.views import lista_objetos

def lista_ingredientes(request):
    nome = request.GET.get('nome')  # Obtenção dos parâmetros do request
    consulta = Q(nome__icontains=nome)
    return lista_objetos(request, [nome], Ingrediente, 'listagem_ingredientes.html', 'ingredientes', consulta)