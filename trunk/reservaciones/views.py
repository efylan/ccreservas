# coding: latin1
from django.shortcuts import render_to_response, HttpResponseRedirect
from django.template import RequestContext
from django.contrib import messages
from aulas.models import Aula, Aplicacion, Equipo
from reservaciones.models import Alumno, Docente, Carrera, Reservacion, Practica, Horario, Clase
from reservaciones.forms import ResEquipoForm, get_now_start, get_now_end, PracticaForm
from django.db.models import Q
import datetime
from ccreservas.utils import get_query
# Create your views here.


def home(request):
    aulas = Aula.get_active.all()
    return render_to_response('reservas_index.html', {'aulas':aulas}, RequestContext(request))

def view_aulas_datetime(request, date, time):
    try:
        aula = Aula.objects.get(id=aula_id)
    except Aula.DoesNotExist:
        messages.error(request, 'Aula no existente.')
        return HttpResponseRedirect('/reservaciones/')

    aulas = Aula.get_active.all().values()
    reservas = self.reservacion_set.filter(Q(fecha=fecha) & Q(hora_inicio__lte=hr_ini) & Q(hora_fin__gte=hr_fin) & Q(activo=1))
    
    for reserva in reservas:
        pass
        
    return render_to_response('reservas_index.html', {'aulas':aulas}, RequestContext(request))

def aula_detail(request, aula_id):
    try:
        aula = Aula.objects.get(id=aula_id)
    except Aula.DoesNotExist:
        messages.error(request, 'Aula no existente.')
        return HttpResponseRedirect('/reservaciones/')

    id_equipos = aula.equipo_set.filter(activo=1).values_list('id')
    fechahora= datetime.datetime.now()
    hoy = fechahora.date()

    reservas = Reservacion.objects.filter(Q(equipo__aula=aula) & Q(fecha=hoy) & Q(hora_inicio__lte=fechahora.time()) & Q(hora_fin__gte=fechahora.time()) & Q(activo=1)).values_list('equipo')
    reservados = []

    aula_disponible = aula.disponible(hoy, fechahora.time(), fechahora.time())

    for reserva in reservas:
        if reserva in id_equipos:
            reservados.append(reserva[0])

    return render_to_response('reservas_aula.html', {'aula':aula, 'reservados':reservados, 'aula_disponible':aula_disponible}, RequestContext(request))

def equipo_reservar_ahora(request, equipo_id):
    try:
        equipo = Equipo.objects.get(id=equipo_id)
    except Equipo.DoesNotExist:
        messages.error(request, 'Equipo no existente.')
        return HttpResponseRedirect('/reservaciones/')
    if request.POST:
        f = ResEquipoForm(request.POST)
        if f.errors:
            return render_to_response('reservas_equipo_ahora.html', {'equipo':equipo, 'form':f}, RequestContext(request))
        else:
            reserva = f.save(commit=False)
            if equipo.disponible(reserva.fecha, reserva.hora_inicio, reserva.hora_fin):
                reserva.equipo=equipo
                f.save()
                messages.success(request,'Reservación creada con exito')
                if 'add_another' in request.POST.keys():
                    return HttpResponseRedirect('/reservaciones/aula/%s/' % equipo.aula.id)
                else:
                    return HttpResponseRedirect('/reservaciones/')
            else:
                messages.warning(request,'El equipo ya está reservado para el %s entre las %s y las %s hrs.' % (reserva.fecha, reserva.hora_inicio, reserva.hora_fin))
                return render_to_response('reservas_equipo_ahora.html', {'equipo':equipo, 'form':f}, RequestContext(request))                

    else:
        f = ResEquipoForm()
        return render_to_response('reservas_equipo_ahora.html', {'equipo':equipo, 'form':f}, RequestContext(request))

def equipo_terminar_actual(request, equipo_id):
    try:
        equipo = Equipo.objects.get(id=equipo_id)
    except Equipo.DoesNotExist:
        messages.error(request, 'Equipo no existente.')
        return HttpResponseRedirect('/reservaciones/')
    
    res = equipo.get_reserva(datetime.date.today(), get_now_start, get_now_end)
    if res == None:
        messages.error(request, 'El equipo %s no esta reservado actualmente.' % (equipo.nombre))
    else:
        hr_term = datetime.datetime.now().time()
        res.hora_fin = datetime.time(hour=hr_term.hour, minute=hr_term.minute)
        messages.warning(request, 'Terminada la reserva del equipo %s de %s a %s' % (equipo.nombre, res.hora_inicio, res.hora_fin))
        res.save()
    return HttpResponseRedirect('/reservaciones/aula/%s/' % equipo.aula.id)


def aula_programar_practica(request, aula_id):
    try:
        aula = Aula.objects.get(id=aula_id)
    except Aula.DoesNotExist:
        messages.error(request, 'Aula no existente.')
        return HttpResponseRedirect('/reservaciones/')
    fechahora= datetime.datetime.now()
    hoy = fechahora.date()
    if request.POST:
        f = PracticaForm(request.POST)
        if f.errors:
            return render_to_response('aula_programar_practica.html', {'aula':aula, 'form':f}, RequestContext(request))
        else:
            practica = f.save(commit=False)
            if aula.disponible(practica.fecha, practica.hora_inicio, practica.hora_fin):
                practica.aula = aula
                practica.save()
                reservas = Reservacion.objects.filter(Q(equipo__aula=aula) & Q(fecha=practica.fecha) & Q(hora_inicio__lte=practica.hora_fin) & Q(hora_fin__gte=practica.hora_inicio) & Q(activo=1))
                reservas_count = reservas.count()

                messages.success(request, 'Práctica programada exitosamente.')
                if reservas.count > 0:
                    ahora = datetime.datetime.now().time()
                    for reserva in reservas:
                        if reserva.hora_inicio > ahora:
                            reserva.activo=0
                        else:
                            reserva.hora_fin = ahora
                        reserva.save()
                    messages.warning(request, '%s reservacion(es) fueron dadas por terminadas para programar la práctica' % (reservas_count))
                return HttpResponseRedirect('/reservaciones/')
            else:
                messages.warning(request, 'Ya existe una práctica programada para el aula %s en %s de %s a %s' % (aula.nombre, practica.fecha, practica.hora_inicio, practica.hora_fin))

                return HttpResponseRedirect('/reservaciones/')

    else:
        id_equipos = aula.equipo_set.filter(activo=1).values_list('id')
        f = PracticaForm()
    
    return render_to_response('aula_programar_practica.html', {'aula':aula, 'form':f}, RequestContext(request))

def busqueda_aplicaciones(request,aula_id):
    try:
        aula = Aula.objects.get(id=aula_id)
    except Aula.DoesNotExist:
        messages.error(request, 'Aula no existente.')
        return HttpResponseRedirect('/reservaciones/')

    query_string = ''
    if ('search' in request.GET) and request.GET['search'].strip():
        query_string = request.GET['search']
        entry_query = get_query(query_string, ['aplicaciones__nombre', 'sistema_operativo'])
        entry_query.connector='OR'
        equipos = aula.equipo_set.filter(entry_query)
        return render_to_response('aplicaciones_buscar.html',
                          { 'query_string': query_string, 'resultados': equipos ,'aula':aula},
                          context_instance=RequestContext(request))    
    else:
        return HttpResponseRedirect('/reservaciones/')

def busqueda_aplicaciones_all(request):
    query_string = ''
    if ('search' in request.GET) and request.GET['search'].strip():

        aulas = Aula.get_active.all()
        aula_list=[]
        query_string = request.GET['search']
        entry_query = get_query(query_string, ['aplicaciones__nombre', 'sistema_operativo'])
        entry_query.connector='OR'

        for aula in aulas:
            aula_dict={}
            aula_dict['aula'] = aula
            equipos = aula.equipo_set.filter(entry_query).distinct()
            aula_dict['equipos'] = equipos
            aula_list.append(aula_dict)

        return render_to_response('aplicaciones_buscar_all.html',
                          { 'query_string': query_string, 'resultados': aula_list},
                          context_instance=RequestContext(request))    
    else:
        return HttpResponseRedirect('/reservaciones/')

def cancelar_practica(request, practica_id):
    try:
        practica = Practica.get_active.get(id=practica_id)
    except Aula.DoesNotExist:
        messages.error(request, 'Práctica no existente.')
        return HttpResponseRedirect('/reservaciones/')
    if request.POST:
        now = datetime.datetime.now()
        if practica.fecha < now.date() and practica.hora_fin < now.time():
            messages.warning(request, 'La práctica ya terminó.')
        else:
            practica.activo=0
            practica.save()
            if 'add_another' in request.POST:
                return HttpResponseRedirect('/reservaciones/aula/%s/practicas/' % practica.aula.id)
            else:
                return HttpResponseRedirect('/reservaciones/')
    else:
        return HttpResponseRedirect('/reservaciones/aula/%s/practicas/' % practica.aula.id)

def ver_reservaciones(request,aula_id):
    try:
        aula = Aula.objects.get(id=aula_id)
    except Aula.DoesNotExist:
        messages.error(request, 'Aula no existente.')
        return HttpResponseRedirect('/reservaciones/')

    fechahora=datetime.datetime.now()
    hoy = fechahora.date()

    reservas = Reservacion.objects.filter((Q(equipo__aula=aula) & Q(fecha__gt=hoy) | Q(hora_fin__gte=fechahora.time(), fecha__gte=hoy)) & Q(activo=1)).order_by('fecha','hora_inicio')

    return render_to_response('ver_reservaciones.html', {'reservas':reservas, 'aula':aula}, RequestContext(request))

def ver_practicas(request, aula_id):
    try:
        aula = Aula.objects.get(id=aula_id)
    except Aula.DoesNotExist:
        messages.error(request, 'Aula no existente.')
        return HttpResponseRedirect('/reservaciones/')

    fechahora=datetime.datetime.now()
    hoy = fechahora.date()

    practicas = aula.practica_set.filter((Q(fecha__gt=hoy) | Q(hora_fin__gte=fechahora.time(),fecha__gte=hoy)) & Q(activo=1)).order_by('fecha','hora_inicio')

    return render_to_response('ver_practicas.html', {'practicas':practicas, 'aula':aula}, RequestContext(request))

def cancelar_reservacion(request, reserva_id):
    try:
        reserva = Reservacion.objects.get(id=reserva_id)
    except Reservacion.DoesNotExist:
        messages.error(request, 'Reservación no existente.')
        return HttpResponseRedirect('/reservaciones/')
    aula_id=reserva.equipo.aula.id
    if request.POST:
        reserva.activo=0
        reserva.save()
        messages.warning(request, 'La reserva para el equipo %s del %s de %s a %s ha sido cancelada.' % (reserva.equipo.nombre, reserva.fecha, reserva.hora_inicio, reserva.hora_fin))
        return HttpResponseRedirect('/reservaciones/aula/%s/ver_reservaciones/' % aula_id)
    else:    
        return HttpResponseRedirect('/reservaciones/')

def cancelar_practica(request, practica_id):
    try:
        practica = Practica.objects.get(id=practica_id)
    except Practica.DoesNotExist:
        messages.error(request, 'Práctica no existente.')
        return HttpResponseRedirect('/reservaciones/')
    aula_id=practica.aula.id
    practica.activo=0
    practica.save()
    messages.warning(request, 'La practica %s del %s de %s a %s ha sido cancelada.' % (practica.nombre, practica.fecha, practica.hora_inicio, practica.hora_fin))
    if request.POST:
        return HttpResponseRedirect('/reservaciones/aula/%s/ver_practicas/' % aula_id)
    else:    
        return HttpResponseRedirect('/reservaciones/')

def terminar_practica(request, practica_id):
    try:
        practica = Practica.objects.get(id=practica_id)
    except Practica.DoesNotExist:
        messages.error(request, 'Practica no existente.')
        return HttpResponseRedirect('/reservaciones/')

    hr_term = datetime.datetime.now().time()
    if practica.hora_fin < hr_term:
        messages.error(request, 'La practica %s del %s de %s a %s ya ha terminado.' % (practica.nombre, practica.fecha, practica.hora_inicio, practica.hora_fin))
    elif practica.hora_inicio > hr_term:
        messages.error(request, 'La practica %s del %s de %s a %s aun no ha empezado.' % (practica.nombre, practica.fecha, practica.hora_inicio, practica.hora_fin))
    else:
        aula_id=practica.aula.id
        practica.hora_fin=datetime.time(hour=hr_term.hour, minute=hr_term.minute)
        practica.save()
        messages.warning(request, 'La practica %s del %s de %s a %s ha sido terminada a la hora actual.' % (practica.nombre, practica.fecha, practica.hora_inicio, practica.hora_fin))
    return HttpResponseRedirect('/reservaciones/')

def equipo_cancelar_actual(request, equipo_id):
    try:
        equipo = Equipo.objects.get(id=equipo_id)
    except Equipo.DoesNotExist:
        messages.error(request, 'Equipo no existente.')
        return HttpResponseRedirect('/reservaciones/')
    
    res = equipo.get_reserva(datetime.date.today(), get_now_start, get_now_end)
    if res == None:
        messages.error(request, 'El equipo %s no esta reservado actualmente.' % (equipo.nombre))
    else:
        res.activo = 0
        res.save()
        messages.warning(request, 'Cancelada la reserva del equipo %s de %s a %s' % (equipo.nombre, res.hora_inicio, res.hora_fin))
    return HttpResponseRedirect('/reservaciones/aula/%s/' % equipo.aula.id)

