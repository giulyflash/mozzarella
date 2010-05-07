from django.conf.urls.defaults import *
from django.views.generic.create_update import create_object
from django.views.generic.list_detail import object_list
from modulo_funcionarios.models import Funcionario

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    (r'^funcionario/cria/', create_object, {'model': Funcionario, 'template_name': 'criacao_funcionario.html'}),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs'
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)
