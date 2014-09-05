# -*- encoding: UTF-8 -*-

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from sigidi import SigidiUserPermissions

# Create your views here.

@login_required
def index(request):
    context = dict()
    list_projects = SigidiUserPermissions(request.user).get_projects()
    return render(request, 'accounting/base.html', context)