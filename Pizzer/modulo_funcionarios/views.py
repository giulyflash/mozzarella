from django.http import Http404
from django.views.generic import list_detail
from modulo_funcionarios.models import Funcionario

def funcionarios_por_nome(request, nome_funcionario):


    try:
        funcionario = Funcionario.objects.get(nome=nome_funcionario)
    except Funcionario.DoesNotExist:
        raise Http404

    return list_detail.object_list(
        request,
        queryset = Funcionario.objects.filter(nome=nome_funcionario),
        template_name = "funcionarios/listagem_funcionarios.html",
        template_object_name = "funcionarios",
    )
