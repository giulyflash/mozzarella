# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *
from django.views.generic.create_update import update_object, delete_object
from models import Funcionario, FuncionarioEditaForm
from views import *

urlpatterns = patterns('',
    (r'^funcionario/cria/', cria_funcionario),
    (r'^funcionario/edita/(?P<object_id>\d+)/$', edita_funcionario),
    (r'^funcionario/deleta/(?P<object_id>\d+)/$', delete_object, {'model': Funcionario, 'template_name': 'confirmacao_delecao.html',
                                                                 'post_delete_redirect': '/pizzer/funcionarios/', 'extra_context': {'model': Funcionario}}),
    (r'^funcionarios/', lista_funcionarios),
)
