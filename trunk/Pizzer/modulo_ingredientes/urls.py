from django.conf.urls.defaults import *
from django.views.generic.create_update import create_object
from django.views.generic.list_detail import object_list
from models import Ingrediente
from views import lista_ingredientes

model_info = {
    "model": Ingrediente,
    "template_name": "criacao_ingrediente.html"
}

urlpatterns = patterns('',
    (r'^ingrediente/cria/', create_object, model_info),
    (r'^ingredientes/', lista_ingredientes),
)