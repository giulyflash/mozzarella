# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *

from modulo_bebidas.models import Bebida
from views import *

urlpatterns = patterns('',
    (r'^bebida/cria/$', cria_bebida),
    (r'^bebida/edita/(?P<object_id>\d+)/$', edita_bebida),
    (r'^bebida/deleta/(?P<object_id>\d+)/$', deleta_bebida),
    (r'^bebidas/$', lista_bebidas)
)