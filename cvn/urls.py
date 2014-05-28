# -*- encoding: UTF-8 -*-

from django.conf.urls import patterns, url

urlpatterns = patterns(
    'cvn.views',
    url(r'^$', 'index', name='cvn'),
    url(r'^ull_report/$', 'ull_report', name='ull_report'),
    url(r'^download/$', 'download_cvn', name='download_cvn'),
    url(r'^stats_report/$', 'stats_report', name='stats_report'),
)
