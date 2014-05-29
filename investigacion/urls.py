# -*- encoding: utf-8 -*-

from django.conf import settings as st
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView, RedirectView
from django.views.generic.detail import DetailView
from django.contrib.flatpages.models import FlatPage


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
    url(r'^investigacion/faq/$', TemplateView.as_view(
        template_name='core/faq.html'), name='faq'),
    url(r'^investigacion/faq/(?P<pk>\d+)/$', DetailView.as_view(
        template_name='core/question_faq.html', model=FlatPage),
        name='question_faq'),
    url(r'^investigacion/tinymce/', include('tinymce.urls')),
)
if st.DEVEL:
    urlpatterns += static(st.MEDIA_URL, document_root=st.MEDIA_ROOT)
    if 'rosetta' in st.INSTALLED_APPS:
        urlpatterns += patterns(
            '',
            url(r'^rosetta/', include('rosetta.urls')),
        )
