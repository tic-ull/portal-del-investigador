# -*- encoding: utf-8 -*-

from django.conf import settings as st
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView, RedirectView

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^investigacion/$', RedirectView.as_view(
        url=st.BASE_URL), name='index'),
    url(r'^investigacion/admin/', include(admin.site.urls)),
    url(r'^investigacion/cvn/', include('cvn.urls')),
    url(r'^investigacion/accounts/login/$',
        'django_cas.views.login', name='login'),
    url(r'^investigacion/accounts/logout/$',
        'django_cas.views.logout', name='logout'),
)
if st.DEVEL:
    urlpatterns += static(st.MEDIA_URL, document_root=st.MEDIA_ROOT)
    if 'rosetta' in st.INSTALLED_APPS:
        urlpatterns += patterns(
            '',
            url(r'^rosetta/', include('rosetta.urls')),
        )
