# -*- coding: utf-8 -*-

from django.db.models import Q
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic.create_update import create_object, update_object, delete_object

from models import Reclamacao, ReclamacaoFormCliente, ReclamacaoFormGerente

from utils.views import lista_objetos
from views import *

@permission_required('modulo_reclamacoes.pode_ver_reclamacoes')
@login_required
def lista_reclamacoes(request):
    status_dict = {
    'A': 'Não Lidas',
    'B': 'Em Investigação',
    'C': 'Incoerentes',
    'D': 'Plausíveis',
    'E': 'Resolvidas',
    'F': ''
    }
    status = request.GET.get('status')
    assunto = request.GET.get('assunto')
    texto = request.GET.get('texto')
    consulta = Q(assunto__icontains=assunto) & Q(texto__icontains=texto)  # Busca pelo assunto especificado e/ou um trecho dentro do texto
    if not status:
        status = 'A'
    if status == 'F':
        universo = None
    else:
        universo = Q(status=status)
    return lista_objetos(request, [assunto, texto], Reclamacao, 'listagem_reclamacoes.html', 'reclamacoes', consulta,
                         universo, 'Exibindo todas as reclamações ' + status_dict[status].upper())

@permission_required('modulo_reclamacoes.pode_resolver_reclamacao')
@login_required
def resolve_reclamacao(request, object_id):
    reclamacao = Reclamacao.objects.get(pk=object_id)
    if request.method == 'POST':
        form = ReclamacaoFormGerente(request.POST)
        if form.is_valid():
            status = form.cleaned_data['status']
            reclamacao.status = status
            reclamacao.save()
            return HttpResponseRedirect('/pizzer/reclamacoes/')
    form = ReclamacaoFormGerente(instance=reclamacao)
    return render_to_response('resolucao_reclamacao.html', {'form': form, 'reclamacao': reclamacao},
                              context_instance=RequestContext(request))

@permission_required('modulo_reclamacoes.pode_criar_reclamacao')
@login_required
def cria_reclamacao(request):
    if request.method == 'POST':
        form = ReclamacaoFormCliente(request.POST)
        if form.is_valid():
            assunto = form.cleaned_data['assunto']
            texto = form.cleaned_data['texto']
            cliente = request.user.cliente_set.all()[0]
            reclamacao = Reclamacao(assunto=assunto, cliente=cliente, texto=texto, status='A')
            reclamacao.save()
            return render_to_response('confirmacao_reclamacao.html', context_instance=RequestContext(request))
    else:
        form = ReclamacaoFormCliente()
    return render_to_response('criacao_reclamacao.html', {'form': form}, context_instance=RequestContext(request))

@permission_required('modulo_reclamacoes.pode_deletar_reclamacao')
@login_required
def deleta_reclamacao(request, object_id):
    return delete_object(request, Reclamacao, '/pizzer/reclamacoes/', object_id, template_name='confirmacao_delecao.html', extra_context={'model': Reclamacao})