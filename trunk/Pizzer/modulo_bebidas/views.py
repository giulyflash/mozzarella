# -*- coding: utf-8 -*-

from models import Bebida
from django.db.models import Q

from utils.views import lista_objetos

def lista_bebidas(request):
    nome = request.GET.get('nome')  # Obten��o dos par�metros do request
    consulta = Q(nome__icontains=nome)
    return lista_objetos(request, [nome], Bebida, 'listagem_bebidas.html', 'bebidas', consulta)# Create your views here.
