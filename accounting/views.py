# -*- encoding: UTF-8 -*-

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from sigidi import SigidiConnection

# Create your views here.

@login_required
def index(request):
    context = dict()
    context['list_projects'] = SigidiConnection(request.user).get_projects()
    print context['list_projects']
    return render(request, 'accounting/index.html', context)