from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    url(r'^$', 'reservaciones.views.home', name='r_home'),
    url(r'^aula/(?P<aula_id>\d+)/$', 'reservaciones.views.aula_detail', name='aula_d'),
    url(r'^aula/(?P<aula_id>\d+)/programar_practica/$', 'reservaciones.views.aula_programar_practica', name='aula_pp'),
    url(r'^aula/(?P<aula_id>\d+)/busqueda_aplicaciones/$', 'reservaciones.views.busqueda_aplicaciones', name='aula_ba'),
    url(r'^aula/busqueda_aplicaciones/$', 'reservaciones.views.busqueda_aplicaciones_all', name='aula_ball'),
    url(r'^aula/(?P<aula_id>\d+)/ver_reservaciones/$', 'reservaciones.views.ver_reservaciones', name='aula_vr'),
    url(r'^aula/(?P<aula_id>\d+)/ver_practicas/$', 'reservaciones.views.ver_practicas', name='aula_vp'),

    url(r'^equipo/(?P<equipo_id>\d+)/ahora/$', 'reservaciones.views.equipo_reservar_ahora', name='equipo_ra'),
    url(r'^equipo/(?P<equipo_id>\d+)/terminar_actual/$', 'reservaciones.views.equipo_terminar_actual', name='equipo_ta'),
    url(r'^equipo/(?P<equipo_id>\d+)/cancelar_actual/$', 'reservaciones.views.equipo_cancelar_actual', name='equipo_ca'),
    url(r'^reservacion/(?P<reserva_id>\d+)/cancelar/$', 'reservaciones.views.cancelar_reservacion', name='reserva_c'),

    url(r'^practica/(?P<practica_id>\d+)/cancelar/$', 'reservaciones.views.cancelar_practica', name='practica_c'),
    url(r'^practica/(?P<practica_id>\d+)/terminar/$', 'reservaciones.views.terminar_practica', name='practica_t'),


)
