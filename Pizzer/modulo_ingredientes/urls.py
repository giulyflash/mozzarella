# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *
from django.views.generic.create_update import create_object, update_object, delete_object

from models import Ingrediente
from views import lista_ingredientes

urlpatterns = patterns('',
    (r'^ingrediente/cria/', create_object, {'model': Ingrediente, 'template_name': 'criacao_ingrediente.html'}),
    (r'^ingrediente/edita/(?P<object_id>\d+)/$', update_object, {'model': Ingrediente, 'template_name': 'edicao_ingrediente.html'}),
    (r'^ingrediente/deleta/(?P<object_id>\d+)/$', delete_object, {'model': Ingrediente, 'template_name': 'confirmacao_delecao.html',
                                                                 'post_delete_redirect': '/pizzer/ingredientes/', 'extra_context': {'model': Ingrediente}}),
    (r'^ingredientes/', lista_ingredientes),
)