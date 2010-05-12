from django.conf.urls.defaults import *
from django.views.generic.create_update import create_object
from modulo_bebidas.models import Bebidas
from views import *

urlpatterns = patterns('',
    # Example:
    (r'^bebida/cria/$', create_object, {'model': Bebidas, 'template_name': 'criacao_bebida.html'}),
    (r'^bebida/edita/(?P<object_id>\d+)/$', update_object, {'model': Cliente, 'template_name': 'edicao_bebida.html'}),
    (r'^bebida/deleta/(?P<object_id>\d+)/$', delete_object, {'model': Cliente, 'template_name': 'confirmacao_delecao.html',
                                                                 'post_delete_redirect': '/pizzer/clientes/', 'extra_context': {'model': Bebida}}),
    (r'^bebidas/$', lista_bebidas)
)