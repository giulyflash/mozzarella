# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *
from modulo_pizzas.models import Pizza
from views import *

urlpatterns = patterns('',
    (r'^pizza/cria/$', cria_pizza),
    (r'^pizza/edita/(?P<object_id>\d+)/$', edita_pizza),
    (r'^pizza/deleta/(?P<object_id>\d+)/$', deleta_pizza),
    (r'^pizzas/', lista_pizzas),


)
