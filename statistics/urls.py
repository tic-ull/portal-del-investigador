# -*- encoding: UTF-8 -*-

from django.conf.urls import patterns, url
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView

urlpatterns = patterns(
    'statistics.views',
    url(r'^$', RedirectView.as_view(url=reverse_lazy('dept_stats')),
        name='statistics'),
    url(r'^departamentos/$', 'dept_stats', name='dept_stats'),
    url(r'^departamentos/(?P<codigo>\d+)/$', 'dept_stats_detail',
        name='dept_stats_detail'),
    url(r'^areas/$', 'area_stats', name='area_stats'),
    url(r'^areas/(?P<codigo>\d+)/$', 'area_stats_detail',
        name='area_stats_detail'),
)
