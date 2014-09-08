# -*- encoding: UTF-8 -*-

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from sigidi import SigidiConnection


@login_required
def index(request):
    context = dict()
    context['list_projects'] = []
    list_projects = SigidiConnection(request.user).get_projects()
    for project in list_projects:
        if project['CONT_KEY'] is not None:
            context['list_projects'].append(project)
    return render(request, 'accounting/index.html', context)
