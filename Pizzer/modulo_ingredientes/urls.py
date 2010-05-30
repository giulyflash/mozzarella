# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *

from models import Ingrediente
from views import *

urlpatterns = patterns('',
    (r'^ingrediente/cria/', cria_ingrediente),
    (r'^ingrediente/edita/(?P<object_id>\d+)/$', edita_ingrediente),
    (r'^ingrediente/deleta/(?P<object_id>\d+)/$', deleta_ingrediente),
    (r'^ingredientes/', lista_ingredientes),
)