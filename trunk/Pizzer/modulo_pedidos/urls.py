from django.conf.urls.defaults import *
from django.views.generic.create_update import create_object, update_object, delete_object
from modulo_pedidos.models import Pedido
from views import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    (r'^pedido/cria/$', create_object, {'model': Pedido, 'template_name': 'criacao_pedido.html'}),
    #(r'^pedido/edita/(?P<object_id>\d+)/$', update_object, {'model': Pedido, 'template_name': 'edita_pedido.html'}),
    #(r'^pedido/deleta/(?P<object_id>\d+)/$', delete_object, {'model': Pedido, 'template_name': 'confirmacao_delecao.html',
    #                                                             'post_delete_redirect': '/pizzer/pedidos/', 'extra_context': {'model': Pedido}}),
    #(r'^pedidos/$', lista_pedidos)

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs'
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)