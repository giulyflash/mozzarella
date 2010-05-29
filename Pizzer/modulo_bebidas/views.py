# -*- coding: utf-8 -*-

from django.db.models import Q

from models import Bebida
from utils.views import lista_objetos

def lista_bebidas(request):
    nome = request.GET.get('nome')  # Obtenção dos parâmetros do request
    consulta = Q(nome__icontains=nome)
    return lista_objetos(request, [nome], Bebida, 'listagem_bebidas.html', 'bebidas', consulta)
