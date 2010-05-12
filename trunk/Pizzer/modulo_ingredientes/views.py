# -*- coding: utf-8 -*-
from django.views.generic import list_detail
from models import Ingrediente

def lista_ingredientes(request):
    nome = request.GET.get('nome') #recupera o parametro 'nome' na query string
    if nome:
        queryset = Ingrediente.objects.filter(nome__contains=nome); #filtro de ingredientes por nome
    else:
        queryset = Ingrediente.objects.all();
    return list_detail.object_list(request,
        queryset=queryset,
        template_name="listagem_ingredientes.html",
        template_object_name="ingredientes")