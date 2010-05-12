# -*- coding: utf-8 -*-

from models import Reclamacao
from django.db.models import Q

from utils.views import lista_objetos

def lista_reclamacoes(request):
    assunto = request.GET.get('assunto')  # Obtenção dos parâmetros do request
    texto = request.GET.get('texto')
    consulta = Q(assunto__icontains=assunto) & Q(texto__icontains=texto)  # Busca pelo assunto especificado e/ou um trecho dentro do texto
    return lista_objetos(request, [assunto, texto], Reclamacao, 'listagem_reclamacoes.html', 'reclamacoes', consulta)