# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *
from modulo_pedidos.models import Pedido
from views import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    (r'^pedido/cria/$', cria_pedido),
    (r'^pedido/edita/(?P<object_id>\d+)/$', edita_pedido),
    (r'^pedido/deleta/(?P<object_id>\d+)/$', deleta_pedido),
    (r'^pedidos/$', lista_pedidos),
    (r'^pedido/cria/pagamento/(?P<object_id>\d+)/$', pagamento),

    (r'^pda/pedido/cria/$', cria_pedido_pda),
    #(r'^pda/pedido/deleta/(?P<object_id>\d+)/$', delete_object, {'model': Pedido, 'template_name': 'confirmacao_delecao.html',
    #                                                         'post_delete_redirect': '/pizzer/pedidos/',
    #                                                         'extra_context': {'model': Pedido}}),
    #(r'^pda/pedidos/$', lista_pedidos_pda),

    (r'^pda2/pedido/edita/(?P<object_id>\d+)/$', edita_pedido_pda2),
    (r'^pda2/pedidos/$', lista_pedidos_pda2),

    (r'^smartphone/pedido/edita/(?P<object_id>\d+)/$', edita_pedido_smartphone),
    (r'^smartphone/pedidos/$', lista_pedidos_smartphone)

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs'
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)
