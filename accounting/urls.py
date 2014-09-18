# -*- encoding: UTF-8 -*-

from django.conf.urls import patterns, url

urlpatterns = patterns(
    'accounting.views',
    url(r'^$', 'index', name='accounting'),
    url(r'^(?P<code>[\w\-]+)/$', 'accounting_detail', name='accounting_detail'),
)
