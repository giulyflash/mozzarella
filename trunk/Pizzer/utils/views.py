# -*- coding: utf-8 -*-

from django.views.generic import list_detail
from django.shortcuts import render_to_response

def lista_objetos(request, parametros, model, template_name, template_object_name, consulta, universo=None):
    mensagem = ''
    nenhum_param_enviado = True
    if request.method == 'POST':
        raise Exception('Essa view não pode ser acessada via POST')
    for parametro in parametros:
        if parametro:  # Se qualquer parâmetro tiver sido usado:
            nenhum_param_enviado = False
            break
    if nenhum_param_enviado:
        if universo:
            queryset = model.objects.filter(universo);
        else:
            queryset = model.objects.all();
        if queryset:
            mensagem = 'Exibindo todos os registros.'
        else:
            mensagem = 'Não há registros a serem exibidos.'
    else:
        if universo:
            queryset = model.objects.filter(consulta & universo);
        else:
            queryset = model.objects.filter(consulta);
        if queryset:
            if len(queryset) > 1:
                mensagem = 'Foram encontrados %d resultados' % len(queryset)
            else:
                mensagem = 'Foi encontrado %d resultado' % len(queryset)
        else:
            mensagem = 'Nenhum registrado foi encontrado.'
    return list_detail.object_list(request,
    queryset=queryset,
    template_name=template_name,
    template_object_name=template_object_name, extra_context={'mensagem': mensagem})



    if not queryset:
        mensagem = 'Não há registros a serem exibidos.'
    else:
        mensagem = 'Exibindo todos os registros.'
    if queryset:
        return list_detail.object_list(request,
            queryset=queryset,
            template_name=template_name,
            template_object_name=template_object_name, extra_context={'mensagem': mensagem})
    else:
        return render_to_response(template_name, {'mensagem': mensagem})# Create your views here.
