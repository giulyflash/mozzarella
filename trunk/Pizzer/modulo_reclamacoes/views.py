# -*- coding: utf-8 -*-

from django.views.generic import list_detail
from models import Reclamacao

def lista_reclamacoes(request):
    if request.method == 'POST':
        raise Exception('Essa view não pode ser acessada via POST')
    assunto = request.GET.get('assunto')
    if assunto:
        queryset = Reclamacao.objects.filter(assunto__icontains=assunto);
    else:
        queryset = Reclamacao.objects.all();
    return list_detail.object_list(request,
        queryset=queryset,
        template_name="listagem_reclamacoes.html",
        template_object_name="reclamacoes")