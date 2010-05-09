from django.conf.urls.defaults import *
from django.views.generic.create_update import create_object
from django.views.generic.list_detail import object_list
from modulo_funcionarios.models import Funcionario
from modulo_funcionarios.views import funcionarios_por_nome



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
    # Generic Vies create:
    (r'^funcionario/cria/', create_object, model_info),
    (r'^funcionarios/', object_list, funcionario_info),
    (r'^funcionarios/(w+)/', funcionarios_por_nome),
)
