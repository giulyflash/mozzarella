# -*- coding: utf-8 -*-
from django.views.generic import list_detail
from models import Pizza

def lista_pizzas(request):
    nome = request.GET.get('nome') #recupera o parametro 'nome' na query string
    if nome:
        queryset = Pizza.objects.filter(nome__contains=nome); #filtro de funcionarios por nome
    else:
        queryset = Pizza.objects.all();
    return list_detail.object_list(request,
        queryset=queryset,
        template_name="listagem_pizzas.html",
        template_object_name="pizzas")