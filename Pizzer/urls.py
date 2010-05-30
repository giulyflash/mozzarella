# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template, redirect_to
from django.views import static

from modulo_autenticacao.views import index
from utils.views import cria_grupos_usuarios, cria_usuarios

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    (r'^$', redirect_to, {'url': '/pizzer/'}),
    (r'^pizzer/dev/gera/grupos/$', cria_grupos_usuarios),  # Insere os grupos no banco. Rodar apenas na instalação.
    (r'^pizzer/dev/gera/usuarios/$', cria_usuarios),  # Insere clientes e funcionários com suas contas de usuários correspondentes no banco. Rodar apenas para testes.
    #(r'^pizzer/$', direct_to_template, {'template': 'index.html'}),  # Era útil enquanto não havia sistema de permissões
    (r'^pizzer/$', index),
    (r'^pizzer/', include('Pizzer.modulo_autenticacao.urls')),
    (r'^pizzer/', include('Pizzer.modulo_reclamacoes.urls')),
	(r'^pizzer/', include('Pizzer.modulo_funcionarios.urls')),
	(r'^pizzer/', include('Pizzer.modulo_pedidos.urls')),
    (r'^pizzer/', include('Pizzer.modulo_clientes.urls')),
    (r'^pizzer/', include('Pizzer.modulo_bebidas.urls')),
    (r'^pizzer/', include('Pizzer.modulo_pizzas.urls')),
    (r'^pizzer/', include('Pizzer.modulo_ingredientes.urls')),

    (r'^pizzer/media/(?P<path>.*)$', static.serve, {'document_root': 'media'}),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs'
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)
