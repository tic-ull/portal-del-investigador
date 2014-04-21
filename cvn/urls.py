# -*- encoding: UTF-8 -*-

from django.conf.urls import patterns, url

urlpatterns = patterns(
    'cvn.views',
    url(r'^$', 'index', name='index'),
    url(r'^ull_report/$', 'ull_report', name='ull_report'),
    url(r'^download/$', 'download_cvn', name='download_cvn'),
)
