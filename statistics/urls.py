# -*- encoding: UTF-8 -*-

from django.conf.urls import patterns, url

urlpatterns = patterns(
    'statistics.views',
    url(r'^$', 'statistics', name='statistics'),
)
