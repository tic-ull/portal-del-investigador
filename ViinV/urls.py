# -*- encoding: utf-8 -*-

from django.conf import settings as st
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^investigacion/admin/', include(admin.site.urls)),

    # Página principal
    url(r'^investigacion/$', 'cvn.views.main', name='main'),
    url(r'^investigacion/cvn/$', 'cvn.views.index', name='index'),
    url(r'^investigacion/cvn/ull_report/$', 'cvn.views.ull_report',
        name='ull_report'),

    # Descarga de los CVN
    url(r'^investigacion/cvn/download/$',
        'cvn.views.downloadCVN',
        name='downloadCVN'),

    # Login/Logout CAS
    url(r'^investigacion/accounts/login/$',
        'django_cas.views.login',
        name='login'),
    url(r'^investigacion/accounts/logout/$',
        'django_cas.views.logout',
        name='logout'),

) + static(st.MEDIA_URL,
           document_root=st.MEDIA_ROOT)
