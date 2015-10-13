# -*- encoding: utf-8 -*-

#
#    Copyright 2014-2015
#
#      STIC-Investigación - Universidad de La Laguna (ULL) <gesinv@ull.edu.es>
#
#    This file is part of Portal del Investigador.
#
#    Portal del Investigador is free software: you can redistribute it and/or
#    modify it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    Portal del Investigador is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with Portal del Investigador.  If not, see
#    <http://www.gnu.org/licenses/>.
#

from core.admin_basic import basic_admin_site
from django.conf import settings as st
from django.conf.urls import patterns, include, url
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView, RedirectView

import debug_toolbar

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^investigacion/admin/', include(admin.site.urls)),
    url(r'^investigacion/adm/', include(basic_admin_site.urls)),
    url(r'^investigacion/accounts/login/$',
        'django_cas.views.login', name='login'),
    url(r'^investigacion/accounts/logout/$',
        'django_cas.views.logout', name='logout'),
)

urlpatterns += i18n_patterns(
    '',
    url(r'^investigacion/$', RedirectView.as_view(
        url=st.BASE_URL), name='index'),
    url(r'^investigacion/cvn/', include('cvn.urls')),
    url(r'^investigacion/faq/$', TemplateView.as_view(
        template_name='core/faq/faq.html'), name='faq'),
    (r'^investigacion/faq/*', include(
        'django.contrib.flatpages.urls')),
)

if 'impersonate' in st.INSTALLED_APPS:
    urlpatterns += i18n_patterns(
        '',
        url(r'^impersonate/', include('impersonate.urls')),
    )

if 'accounting' in st.INSTALLED_APPS:
    urlpatterns += i18n_patterns(
        '',
        url(r'^investigacion/contabilidad/', include('accounting.urls')),
    )

if 'statistics' in st.INSTALLED_APPS:
    urlpatterns += i18n_patterns(
        '',
        url(r'^investigacion/estadisticas/', include('statistics.urls')),
    )

if st.DEVEL:
    urlpatterns += static(st.MEDIA_URL, document_root=st.MEDIA_ROOT)
    urlpatterns += static(st.STATIC_URL, document_root=st.STATIC_ROOT)

if st.DEBUG:
    if 'rosetta' in st.INSTALLED_APPS:
        urlpatterns += patterns(
            '',
            url(r'^investigacion/rosetta/', include('rosetta.urls')),
        )

    if 'debug_toolbar' in st.INSTALLED_APPS:
        urlpatterns += patterns(
            '',
            url(r'^__debug__/', include(debug_toolbar.urls)),
        )
