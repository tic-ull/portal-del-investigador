# -*- encoding: utf-8 -*-

from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^investigacion/admin/', include(admin.site.urls)),
    url(r'^investigacion/cvn/', include('cvn.urls')),
    url(r'^investigacion/accounts/login/$',
        'django_cas.views.login', name='login'),
    url(r'^investigacion/accounts/logout/$',
        'django_cas.views.logout', name='logout'),
    url(r'^investigacion/$', RedirectView.as_view(url=reverse_lazy('index')))
)
