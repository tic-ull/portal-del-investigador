# -*- encoding: UTF-8 -*-

from cvn import views
from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',
    url(r'^$', views.index, name='index'),
    url(r'^ull_report/$', views.ull_report, name='ull_report'),
    url(r'^download/$', views.download_cvn, name='download_cvn'),
)
