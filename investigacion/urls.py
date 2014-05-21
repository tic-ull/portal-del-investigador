# -*- encoding: utf-8 -*-

from django.conf import settings as st
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^investigacion/admin/', include(admin.site.urls)),
    url(r'^investigacion/cvn/', include('cvn.urls')),
    url(r'^investigacion/$', 'core.views.index', name='index'),
    url(r'^investigacion/accounts/login/$',
        'django_cas.views.login', name='login'),
    url(r'^investigacion/accounts/logout/$',
        'django_cas.views.logout', name='logout'),
    url(r'^investigacion/faq/', include('django.contrib.flatpages.urls')),
    url(r'^investigacion/tinymce/', include('tinymce.urls')),
    url(r'^investigacion2', TemplateView.as_view(
        template_name='cvn/ccti.html.bak')),
    url(r'^investigacion3', TemplateView.as_view(
        template_name='core/base.html')),
)

#
if st.DEVEL:
    urlpatterns += static(st.MEDIA_URL, document_root=st.MEDIA_ROOT)
