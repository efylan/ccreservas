from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    url(r'^$', 'informes.views.home', name='i_home'),
    url(r'^pendientes/$', 'informes.views.informes_pendientes', name='i_pend'),
    url(r'^arreglados/$', 'informes.views.informes_arreglados', name='i_fixed'),
    url(r'^noarreglados/$', 'informes.views.informes_wontfix', name='i_wontfix'),

    url(r'^equipo/(?P<equipo_id>\d+)/levantar/$', 'informes.views.levantar_informe_equipo', name='informe_le'),
    url(r'^(?P<informe_id>\d+)/resolver/$', 'informes.views.resolver_informe', name='informe_r'),

)
