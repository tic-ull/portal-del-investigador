# -*- encoding: UTF-8 -*-

from django.conf.urls import patterns, url
from django.http import HttpResponse
from .settings import HISTORICAL_YEAR

urlpatterns = patterns(
    'cvn.views',
    url(r'^$', 'index', name='cvn'),
    url(r'^ull_report/$', 'ull_report', {'year': HISTORICAL_YEAR},
        name='ull_report'),
    url(r'^download/$', 'download_cvn', name='download_cvn'),
    url(r'^waiting/$', lambda r: HttpResponse(status=204), name='waiting'),
    url(r'^export_data/$', 'export_data_ull', name='export_data_ull'),
)
