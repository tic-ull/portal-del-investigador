from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def index(request):
    context = dict()
    return render(request, 'accounting/base.html', context)