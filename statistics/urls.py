# -*- encoding: UTF-8 -*-

from django.conf.urls import patterns, url

urlpatterns = patterns(
    'statistics.views',
    url(r'^departamento/$', 'statistics', name='statistics'),
    url(r'^departamento/(?P<codigo>\d+)/$', 'stats_detail', name='stats_detail'),
)
