# -*- coding: utf-8 -*-

from django.db.models import Q
from django.contrib.auth.decorators import login_required, permission_required

from models import Pizza
from utils.views import lista_objetos

@permission_required('modulo_pizzas.pode_ver_pizzas')
@login_required
def lista_pizzas(request):
    nome = request.GET.get('nome')  # Obtenção dos parâmetros do request
    consulta = Q(nome__icontains=nome)
    return lista_objetos(request, [nome], Pizza, 'listagem_pizzas.html', 'pizzas', consulta)