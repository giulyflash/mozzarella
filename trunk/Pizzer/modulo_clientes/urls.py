# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *
from django.views.generic.create_update import update_object, delete_object
from modulo_clientes.models import Cliente, ClienteForm
from views import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    (r'^cliente/cria/$', cria_cliente),
    (r'^cliente/edita/(?P<object_id>\d+)/$', update_object, {'model': Cliente, 'template_name': 'edita_cliente.html'}),
    (r'^cliente/deleta/(?P<object_id>\d+)/$', delete_object, {'model': Cliente, 'template_name': 'confirmacao_delecao.html',
                                                                 'post_delete_redirect': '/pizzer/clientes/', 'extra_context': {'model': Cliente}}),
    (r'^clientes/$', lista_clientes)

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs'
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)
