# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *
from django.views.generic.create_update import create_object, update_object, delete_object
from django.contrib.auth.models import User
from views import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    (r'^usuario/login/$', faz_login),
    (r'^usuario/logout/$', faz_logout),
    (r'^usuario/cria/$', cria_usuario),
    (r'^usuario/edita/(?P<object_id>\d+)/$', edita_usuario),
    (r'^usuario/deleta/(?P<object_id>\d+)/$', delete_object, {'model': User, 'template_name': 'confirmacao_delecao.html',
                                                                 'post_delete_redirect': '/pizzer/usuarios/', 'extra_context': {'model': User}}),
    (r'^usuarios/$', lista_usuarios)

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs'
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)
