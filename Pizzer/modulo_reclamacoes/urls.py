from django.conf.urls.defaults import *
from django.views.generic.create_update import create_object, update_object, delete_object
from modulo_reclamacoes.models import Reclamacao, ReclamacaoFormCliente, ReclamacaoFormGerente
from views import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    (r'^reclamacao/cria/$', create_object, {'form_class': ReclamacaoFormCliente, 'template_name': 'criacao_reclamacao.html'}),
    (r'^reclamacao/resolve/(?P<object_id>\d+)/$', update_object, {'form_class': ReclamacaoFormGerente, 'template_name': 'resolucao_reclamacao.html'}),
    (r'^reclamacao/deleta/(?P<object_id>\d+)/$', delete_object, {'model': Reclamacao, 'template_name': 'confirmacao_delecao.html',
                                                                 'post_delete_redirect': '/pizzer/reclamacoes/', 'extra_context': {'model': Reclamacao}}),
    (r'^reclamacoes/$', lista_reclamacoes)

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs'
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)
