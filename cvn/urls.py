# -*- encoding: utf-8 -*-

from django.conf.urls import patterns, url
from cvn import views

urlpatterns = patterns('',
    # Página principal
    url(r'^$', views.index, name='index'),
    url(r'^ull_report/$', views.ull_report, name='ull_report'),
    url(r'^download/$', views.downloadCVN, name='downloadCVN'),
)
