# -*- encoding: UTF-8 -*-

from django.conf.urls import patterns, url
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView
from django.conf import settings as st

urlpatterns = patterns(
    'statistics.views',

    url(r'^$', RedirectView.as_view(url=reverse_lazy('dept_stats')),
        name='statistics'),

    url(r'^departamentos/$', 'unit_stats',
        {'unit': u'Departamentos', 'model': 'Department'},
        name='dept_stats'),

    url(r'^departamentos/(?P<codigo>\d+)/$', 'unit_stats_detail',
        {'unit': u'Departamentos', 'model': 'Department'},
        name='dept_stats_detail'),

    url(r'^areas/$', 'unit_stats',
        {'unit': u'Áreas', 'model': 'Area'},
        name='area_stats'),

    url(r'^areas/(?P<codigo>\d+)/$', 'unit_stats_detail',
        {'unit': u'Áreas', 'model': 'Area'},
        name='area_stats_detail'),
)
