from django.conf.urls.defaults import *
from django.views.generic.create_update import create_object
from django.views.generic.list_detail import object_list
from modulo_pizzas.models import Pizza
from views import *

model_info = {
    "model": Pizza,
    "template_name": "criacao_pizza.html"
}

urlpatterns = patterns('',
    (r'^pizza/cria/', create_object, model_info),
    (r'^pizzas/', lista_pizzas),
)
