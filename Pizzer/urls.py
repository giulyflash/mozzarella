from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.views import static

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    (r'^pizzer/$', direct_to_template, {'template': 'index.html'}),
    (r'^pizzer/', include('Pizzer.modulo_reclamacoes.urls')),
	(r'^pizzer/', include('Pizzer.modulo_funcionarios.urls')),



    (r'^pizzer/media/(?P<path>.*)$', static.serve, {'document_root': 'media'}),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs'
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)
