# -*- coding: utf-8 -*-
from django.views.generic import list_detail
from models import Funcionario

def lista_funcionarios(request):
    nome = request.GET.get('nome') #recupera o parametro nome na query string
    if nome:
        queryset = Funcionario.objects.filter(nome__contains=nome); #filtro de funcionarios por nome
    else:
        queryset = Funcionario.objects.all();
    return list_detail.object_list(request,
        queryset=queryset,
        template_name="listagem_funcionarios.html",
        template_object_name="funcionarios")