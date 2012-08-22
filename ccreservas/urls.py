from django.conf.urls import patterns, include, url
from ccreservas.settings import MEDIA_ROOT

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'ccreservas.views.home', name='home'),
    url(r'^reservaciones/', include('reservaciones.urls')),
    url(r'^informes/', include('informes.urls')),
    url(r'^administracion/', include('admon.urls')),
    url(r'^reportes/', include('reportes.urls')),
    url(r'^login/', 'ccreservas.views.login', name='login'),
    url(r'^logout/', 'ccreservas.views.logout', name='login'),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('django.views',(r'^media/(?P<path>.*)$', 'static.serve', {'document_root': MEDIA_ROOT}))

