# -*- encoding: UTF-8 -*-

from django.conf.urls import patterns, url

urlpatterns = patterns(
    'accounting.views',
    url(r'^$', 'index', name='accounting'),
)
