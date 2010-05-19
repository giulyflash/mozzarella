from django.conf.urls.defaults import *
from django.views.generic.create_update import create_object, update_object, delete_object
from modulo_bebidas.models import Bebida
from views import *

urlpatterns = patterns('',
    # Example:
    (r'^bebida/cria/$', create_object, {'model': Bebida, 'template_name': 'criacao_bebida.html'}),
    (r'^bebida/edita/(?P<object_id>\w+)/$', update_object, {'model': Bebida, 'template_name': 'edicao_bebida.html'}),
    (r'^bebida/deleta/(?P<object_id>\w+)/$', delete_object, {'model': Bebida, 'template_name': 'confirmacao_delecao.html',
                                                                 'post_delete_redirect': '/pizzer/bebidas/', 'extra_context': {'model': Bebida}}),
    (r'^bebidas/$', lista_bebidas)
)