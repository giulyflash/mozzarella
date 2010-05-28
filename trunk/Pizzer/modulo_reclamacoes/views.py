# -*- coding: utf-8 -*-

from django.db.models import Q
from django.shortcuts import render_to_response

from models import Reclamacao

from utils.views import lista_objetos

def lista_reclamacoes(request):
    assunto = request.GET.get('assunto')  # Obtenção dos parâmetros do request
    texto = request.GET.get('texto')
    consulta = Q(assunto__icontains=assunto) & Q(texto__icontains=texto)  # Busca pelo assunto especificado e/ou um trecho dentro do texto
    return lista_objetos(request, [assunto, texto], Reclamacao, 'listagem_reclamacoes.html', 'reclamacoes', consulta)

def resolve_reclamacao(request, object_id):
    reclamacao = Reclamacao.objects.get(pk=object_id)
    return render_to_response('resolucao_reclamacao.html', {'reclamacao': reclamacao})