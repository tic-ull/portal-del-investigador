# -*- encoding: UTF-8 -*-

from django.conf.urls import patterns, url
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView

urlpatterns = patterns(
    'statistics.views',
    url(r'^$', RedirectView.as_view(url=reverse_lazy(
        'dept_stats')), name='statistics'),
    url(r'^departamentos/$', 'statistics', name='dept_stats'),
    url(r'^departamentos/(?P<codigo>\d+)/$', 'stats_detail',
        name='stats_detail'),
)
