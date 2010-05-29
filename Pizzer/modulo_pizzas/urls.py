# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *
from django.views.generic.create_update import create_object, update_object, delete_object
from django.views.generic.list_detail import object_list
from modulo_pizzas.models import Pizza
from views import *

create_object_info = {
    "model": Pizza,
    "template_name": "criacao_pizza.html"
}

update_object_info = {
    "model": Pizza,
    "template_name": "edicao_pizza.html"
}

delete_object_info = {
    "model": Pizza, "template_name": "confirmacao_delecao.html",
    "post_delete_redirect": "/pizzer/pizzas/",
    "extra_context": {'model': Pizza}
}

urlpatterns = patterns('',
    (r'^pizza/cria/$', create_object, create_object_info),
    (r'^pizza/edita/(?P<object_id>\d+)/$', update_object, update_object_info),
    (r'^pizza/deleta/(?P<object_id>\d+)/$', delete_object, delete_object_info),
    (r'^pizzas/', lista_pizzas),


)
