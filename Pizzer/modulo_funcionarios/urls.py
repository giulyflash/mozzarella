# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *
from django.views.generic.create_update import create_object, update_object, delete_object
from models import Funcionario
from views import *

urlpatterns = patterns('',
    (r'^funcionario/cria/', create_object, {"model": Funcionario, "template_name": "criacao_funcionario.html"}),
    (r'^funcionario/edita/(?P<object_id>\d+)/$', update_object, {'model': Funcionario, 'template_name': 'edicao_funcionario.html'}),
    (r'^funcionario/deleta/(?P<object_id>\d+)/$', delete_object, {'model': Funcionario, 'template_name': 'confirmacao_delecao.html',
                                                                 'post_delete_redirect': '/pizzer/funcionarios/', 'extra_context': {'model': Funcionario}}),
    (r'^funcionarios/', lista_funcionarios),
)
