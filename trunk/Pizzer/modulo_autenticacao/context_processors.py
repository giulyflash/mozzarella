# -*- coding: utf-8 -*-

def group(request):
    if request.user.is_authenticated():
        if request.user.is_superuser:
            group = 'admin'
        else:
            group = request.user.groups.all()[0].name
    else:
        group = 'anônimo'
    return {'group': group}

def is_desktop_group(request):
    if request.user.is_authenticated():
        if request.user.is_superuser:
            group = 'admin'
        else:
            group = request.user.groups.all()[0].name
    else:
        group = 'anônimo'
    return {'is_desktop_group': group in ('admin', 'anônimo', 'cliente', 'gerente', 'atendente')}