from django.conf.urls.defaults import *
from django.views.generic.create_update import create_object
from django.views.generic.list_detail import object_list
from modulo_reclamacoes.models import Pedido

model_info = {
    "model": Pedido,
    "template_name": "pda_criacao_pedido.html"
}

urlpatterns = patterns('',
    (r'^pda/pedido/cria/', create_object, model_info),
)
