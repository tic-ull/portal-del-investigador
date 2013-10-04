# -*- encoding: utf-8 -*-

from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
import cvn.settings as cvn_setts


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^investigacion/$', 'ViinV.views.home', name='home'),
    # url(r'^investigacion/ViinV/', include('ViinV.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^investigacion/admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^investigacion/admin/', include(admin.site.urls)),
    
    # Página principal
    url(r'^investigacion/$', 'cvn.views.main', name='main'),
    
    url(r'^investigacion/cvn/$', 'cvn.views.index', name='index'),
    
    # Login/Logout CAS
    url(r'^investigacion/accounts/login/$', 'django_cas.views.login', name='login'), 
    url(r'^investigacion/accounts/logout/$', 'django_cas.views.logout', name='logout'),
    
    
) + static(cvn_setts.MEDIA_PDF, document_root=cvn_setts.URL_PDF)  # Servir los pdfs
