# -*- coding: utf-8 -*-

from django.db.models import Q
from django.contrib.auth.decorators import login_required, permission_required

from models import Ingrediente
from utils.views import lista_objetos

@login_required
def lista_ingredientes(request):
    nome = request.GET.get('nome')  # Obtenção dos parâmetros do request
    consulta = Q(nome__icontains=nome)
    return lista_objetos(request, [nome], Ingrediente, 'listagem_ingredientes.html', 'ingredientes', consulta)