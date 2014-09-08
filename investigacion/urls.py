# -*- encoding: utf-8 -*-

from django.conf import settings as st
from django.conf.urls import patterns, include, url
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from flatpages_i18n.models import FlatPage_i18n
from django.views.generic import TemplateView, RedirectView
from django.views.generic.detail import DetailView

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^investigacion/$', RedirectView.as_view(
        url=st.BASE_URL), name='index'),
    url(r'^investigacion/admin/', include(admin.site.urls)),
    url(r'^investigacion/accounts/login/$',
        'django_cas.views.login', name='login'),
    url(r'^investigacion/accounts/logout/$',
        'django_cas.views.logout', name='logout'),
    url(r'^investigacion/tinymce/', include('tinymce.urls')),
)

urlpatterns += i18n_patterns(
    '',
    url(r'^investigacion/cvn/', include('cvn.urls')),
    url(r'^investigacion/estadisticas/', include('statistics.urls')),
    url(r'^investigacion/faq/$', TemplateView.as_view(
        template_name='core/faq/faq.html'), name='faq'),
    url(r'^investigacion/faq/(?P<pk>\d+)/$', DetailView.as_view(
        template_name='core/faq/question_faq.html', model=FlatPage_i18n),
        name='question_faq'),
    url(r'^investigacion/contabilidad/', include('accounting.urls')),
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
