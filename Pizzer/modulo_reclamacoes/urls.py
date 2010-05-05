from django.conf.urls.defaults import *
from django.views.generic.create_update import create_object
from django.views.generic.list_detail import object_list
from modulo_reclamacoes.models import Reclamacao

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    (r'^reclamacao/cria/', create_object, {'model': Reclamacao, 'template_name': 'criacao_reclamacao.html'}),
    (r'^reclamacoes/', object_list, {'queryset': Reclamacao.objects.all(), 'template_object_name': 'reclamacoes', 'template_name': 'listagem_reclamacoes.html'}),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs'
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)
