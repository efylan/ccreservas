from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    url(r'^$', 'admon.views.home', name='a_home'),
    url(r'^aulas/crear/$', 'admon.views.aula_create', name='aula_c'),
    url(r'^aulas/editar/(?P<aula_id>\d+)/$', 'admon.views.aula_modify', name='aula_m'),
    url(r'^aulas/$', 'admon.views.aula_list', name='aula_l'),
    url(r'^aulas/advertencia/(?P<aula_id>\d+)/$', 'admon.views.aula_warning', name='aula_w'),
    url(r'^aulas/borrar/(?P<aula_id>\d+)/$', 'admon.views.aula_warning', name='aula_w'),
    #----------------------------------
    url(r'^equipos/crear/$', 'admon.views.equipo_create', name='equipo_c'),
    url(r'^equipos/editar/(?P<equipo_id>\d+)/$', 'admon.views.equipo_modify', name='equipo_m'),
    url(r'^equipos/$', 'admon.views.equipo_list', name='equipo_l'),
    url(r'^equipos/advertencia/(?P<equipo_id>\d+)/$', 'admon.views.equipo_warning', name='equipo_w'),
    url(r'^equipos/borrar/(?P<equipo_id>\d+)/$', 'admon.views.equipo_warning', name='equipo_w'),
    #----------------------------------
    url(r'^aplicaciones/crear/$', 'admon.views.app_create', name='app_c'),
    url(r'^aplicaciones/editar/(?P<app_id>\d+)/$', 'admon.views.app_modify', name='app_m'),
    url(r'^aplicaciones/$', 'admon.views.app_list', name='app_l'),
    url(r'^aplicaciones/advertencia/(?P<app_id>\d+)/$', 'admon.views.app_warning', name='app_w'),
    url(r'^aplicaciones/borrar/(?P<app_id>\d+)/$', 'admon.views.app_warning', name='app_w'),
    #----------------------------------
    url(r'^carreras/crear/$', 'admon.views.carrera_create', name='carrera_c'),
    url(r'^carreras/editar/(?P<carrera_id>\d+)/$', 'admon.views.carrera_modify', name='carrera_m'),
    url(r'^carreras/$', 'admon.views.carrera_list', name='carrera_l'),
    url(r'^carreras/advertencia/(?P<carrera_id>\d+)/$', 'admon.views.carrera_warning', name='carrera_w'),
    url(r'^carreras/borrar/(?P<carrera_id>\d+)/$', 'admon.views.carrera_warning', name='carrera_w'),
    #----------------------------------
    url(r'^alumnos/crear/$', 'admon.views.alumno_create', name='alumno_c'),
    url(r'^alumnos/editar/(?P<alumno_id>\d+)/$', 'admon.views.alumno_modify', name='alumno_m'),
    url(r'^alumnos/$', 'admon.views.alumno_list', name='alumno_l'),
    url(r'^alumnos/advertencia/(?P<alumno_id>\d+)/$', 'admon.views.alumno_warning', name='alumno_w'),
    url(r'^alumnos/borrar/(?P<alumno_id>\d+)/$', 'admon.views.alumno_warning', name='alumno_w'),
    #----------------------------------
    url(r'^docentes/crear/$', 'admon.views.docente_create', name='docente_c'),
    url(r'^docentes/editar/(?P<docente_id>[-\w]+)/$', 'admon.views.docente_modify', name='docente_m'),
    url(r'^docentes/$', 'admon.views.docente_list', name='docente_l'),
    url(r'^docentes/advertencia/(?P<docente_id>[-\w]+)/$', 'admon.views.docente_warning', name='docente_w'),
    url(r'^docentes/borrar/(?P<docente_id>[-\w]+)/$', 'admon.views.docente_warning', name='docente_w'),
    #----------------------------------
    url(r'^users/crear/$', 'admon.views.user_create', name='user_c'),
    url(r'^users/editar/(?P<user_id>\d+)/$', 'admon.views.user_modify', name='user_m'),
    url(r'^users/editar/(?P<user_id>\d+)/password/$', 'admon.views.user_password', name='user_m'),
    url(r'^users/$', 'admon.views.user_list', name='user_l'),
    url(r'^users/advertencia/(?P<user_id>\d+)/$', 'admon.views.user_warning', name='user_w'),
    url(r'^users/borrar/(?P<user_id>\d+)/$', 'admon.views.user_warning', name='user_w'),
   #----------------------------------
    url(r'^groups/crear/$', 'admon.views.group_create', name='group_c'),
    url(r'^groups/editar/(?P<group_id>\d+)/$', 'admon.views.group_modify', name='group_m'),
    url(r'^groups/$', 'admon.views.group_list', name='group_l'),
    url(r'^groups/advertencia/(?P<group_id>\d+)/$', 'admon.views.group_warning', name='group_w'),
    url(r'^groups/borrar/(?P<group_id>\d+)/$', 'admon.views.group_warning', name='group_w'),

)
