from django.conf.urls.defaults import *
from django.views.generic.create_update import create_object
from django.views.generic.list_detail import object_list
from modulo_funcionarios.models import Funcionario
from views import *



funcionario_info = {
    "queryset" : Funcionario.objects.all(),
    "template_object_name" : "funcionarios",
    "template_name" : "listagem_funcionarios.html"
}

model_info = {
    "model": Funcionario,
    "template_name": "criacao_funcionario.html"
}

urlpatterns = patterns('',
    (r'^funcionario/cria/', create_object, model_info),
    (r'^funcionarios/', lista_funcionarios),
)
