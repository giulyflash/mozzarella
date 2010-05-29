# -*- coding: utf-8 -*-

from django.db.models import Q

from models import Funcionario
from utils.views import lista_objetos

def lista_funcionarios(request):
    nome = request.GET.get('nome')  # Obtenção dos parâmetros do request
    consulta = Q(nome__icontains=nome)
    return lista_objetos(request, [nome], Funcionario, 'listagem_funcionarios.html', 'funcionarios', consulta)# Create your views here.