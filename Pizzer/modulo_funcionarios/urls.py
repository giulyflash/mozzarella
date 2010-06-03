# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *
from models import Funcionario, FuncionarioEditaForm
from views import *

urlpatterns = patterns('',
    (r'^funcionario/cria/', cria_funcionario),
    (r'^pessoa/edita/', edita_pessoa),
    (r'^funcionario/edita/(?P<object_id>\d+)/$', edita_funcionario),
    (r'^funcionario/edita/dadospessoais/(?P<object_id>\d+)/$', edita_funcionario_dadospessoais),
    (r'^funcionario/deleta/(?P<object_id>\d+)/$', deleta_funcionario),
    (r'^funcionarios/', lista_funcionarios),
)
