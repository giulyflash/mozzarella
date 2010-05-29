# -*- coding: utf-8 -*-

from django.db.models import Q

from models import Pizza
from utils.views import lista_objetos

def lista_pizzas(request):
    nome = request.GET.get('nome')  # Obtenção dos parâmetros do request
    consulta = Q(nome__icontains=nome)
    return lista_objetos(request, [nome], Pizza, 'listagem_pizzas.html', 'pizzas', consulta)