from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    url(r'^$', 'reportes.views.home', name='rep_home'),
    url(r'^reservaciones/$', 'reportes.views.reporte_reservaciones', name='rep_reservas'),
    url(r'^reservaciones_canceladas/$', 'reportes.views.reporte_reservaciones_canceladas', name='rep_reservas_c'),

    url(r'^practicas/$', 'reportes.views.reporte_practicas', name='rep_practicas'),
    url(r'^practicas_canceladas/$', 'reportes.views.reporte_practicas_canceladas', name='rep_practicas_c'),

    url(r'^informes/$', 'reportes.views.reporte_informes', name='rep_informes'),
    url(r'^inventario/$', 'reportes.views.reporte_inventario', name='rep_inv'),
)
