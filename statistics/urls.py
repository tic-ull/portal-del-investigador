# -*- encoding: UTF-8 -*-

from django.conf.urls import patterns, url

urlpatterns = patterns(
    'statistics.views',
    url(r'^departamentos/$', 'statistics', name='statistics'),
    url(r'^departamentos/(?P<codigo>\d+)/$', 'stats_detail',
        name='stats_detail'),
)
