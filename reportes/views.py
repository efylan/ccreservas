from django.shortcuts import render_to_response, HttpResponseRedirect
from django.template import RequestContext
from django.contrib import messages
from reportes.forms import AulaFechaForm, AulaForm, RepInformeForm
from reservaciones.models import Reservacion, Practica
from informes.models import Informe
from aulas.models import Aula

def home(request):
    return render_to_response('reportes_index.html', {}, RequestContext(request))

def reporte_reservaciones(request):
    titulo = "Reporte de Reservaciones"
    if request.POST:
        f = AulaFechaForm(request.POST)
        if f.errors:
            return render_to_response('f_reporte.html', {'form':f, 'titulo':titulo}, RequestContext(request))        
        else:
            aula = f.cleaned_data['aula']
            fecha_incio = f.cleaned_data['fecha_inicio']
            fecha_fin = f.cleaned_data['fecha_fin']
            hora_inicio = f.cleaned_data['hora_inicio']
            hora_fin = f.cleaned_data['hora_fin']
            return reporte_reservaciones_core(request, aula, fecha_incio, fecha_fin, hora_inicio, hora_fin, titulo = titulo)
    else:
        f = AulaFechaForm()
        return render_to_response('f_reporte.html', {'form':f, 'titulo':titulo}, RequestContext(request))

def reporte_reservaciones_canceladas(request):
    titulo = "Reporte de Reservaciones Canceladas"
    if request.POST:
        f = AulaFechaForm(request.POST)
        if f.errors:
            return render_to_response('f_reporte.html', {'form':f, 'titulo':titulo}, RequestContext(request))        
        else:
            aula = f.cleaned_data['aula']
            fecha_incio = f.cleaned_data['fecha_inicio']
            fecha_fin = f.cleaned_data['fecha_fin']
            hora_inicio = f.cleaned_data['hora_inicio']
            hora_fin = f.cleaned_data['hora_fin']
            return reporte_reservaciones_core(request, aula, fecha_incio, fecha_fin, hora_inicio, hora_fin, titulo = titulo, activo = 0)
    else:
        f = AulaFechaForm()
        return render_to_response('f_reporte.html', {'form':f, 'titulo':titulo}, RequestContext(request))


def reporte_reservaciones_core(request, aula, fecha_inicio, fecha_fin, hora_inicio, hora_fin, activo=1, titulo=""):
    if aula == None:
        if hora_inicio and hora_fin:
            reservas = Reservacion.objects.filter(fecha__range=(fecha_inicio, fecha_fin), activo=activo, hora_inicio__range=(hora_inicio,hora_fin))
        else:
            reservas = Reservacion.objects.filter(fecha__range=(fecha_inicio, fecha_fin), activo=activo)
        aulas = Aula.get_active.all()
    else:
        if hora_inicio and hora_fin:
            reservas = Reservacion.objects.filter(equipo__aula=aula, fecha__range=(fecha_inicio, fecha_fin), activo=activo, hora_inicio__range=(hora_inicio,hora_fin))
        else:
            reservas = Reservacion.objects.filter(equipo__aula=aula, fecha__range=(fecha_inicio, fecha_fin), activo=activo)

        aulas = Aula.get_active.filter(id=aula.id)

    aula_list=[]
    total_count = 0
    for aula in aulas:
        aula_dict={}
        aula_dict['aula'] = aula
        reservas_aula = reservas.filter(equipo__aula=aula)
        aula_dict['reservaciones'] = reservas_aula 
        aula_dict['count'] = reservas_aula.count()
        total_count+=aula_dict['count']
        aula_list.append(aula_dict)

        
    return render_to_response('reporte_reservaciones.html', {'titulo':titulo, 'aula_list':aula_list, 'total_count':total_count}, RequestContext(request))


def reporte_practicas(request):
    titulo = "Reporte de Practicas"
    if request.POST:
        f = AulaFechaForm(request.POST)
        if f.errors:
            return render_to_response('f_reporte.html', {'form':f, 'titulo':titulo}, RequestContext(request))        
        else:
            aula = f.cleaned_data['aula']
            fecha_incio = f.cleaned_data['fecha_inicio']
            fecha_fin = f.cleaned_data['fecha_fin']
            hora_inicio = f.cleaned_data['hora_inicio']
            hora_fin = f.cleaned_data['hora_fin']
            return reporte_practicas_core(request, aula, fecha_incio, fecha_fin, hora_inicio, hora_fin, titulo = titulo)
    else:
        f = AulaFechaForm()
        return render_to_response('f_reporte.html', {'form':f, 'titulo':titulo}, RequestContext(request))

def reporte_practicas_canceladas(request):
    titulo = "Reporte de Practicas Canceladas"
    if request.POST:
        f = AulaFechaForm(request.POST)
        if f.errors:
            return render_to_response('f_reporte.html', {'form':f, 'titulo':titulo}, RequestContext(request))        
        else:
            aula = f.cleaned_data['aula']
            fecha_incio = f.cleaned_data['fecha_inicio']
            fecha_fin = f.cleaned_data['fecha_fin']
            hora_inicio = f.cleaned_data['hora_inicio']
            hora_fin = f.cleaned_data['hora_fin']
            return reporte_practicas_core(request, aula, fecha_incio, fecha_fin, hora_inicio, hora_fin, titulo = titulo, activo=0)
    else:
        f = AulaFechaForm()
        return render_to_response('f_reporte.html', {'form':f, 'titulo':titulo}, RequestContext(request))


def reporte_practicas_core(request, aula, fecha_inicio, fecha_fin, hora_inicio, hora_fin, activo=1, titulo=""):
    if aula == None:
        if hora_inicio and hora_fin:
            practicas = Practica.objects.filter(fecha__range=(fecha_inicio, fecha_fin), activo=activo, hora_inicio__range=(hora_inicio,hora_fin))
        else:
            practicas = Practica.objects.filter(fecha__range=(fecha_inicio, fecha_fin), activo=activo)
        aulas = Aula.get_active.all()
    else:
        if hora_inicio and hora_fin:
            practicas = Practica.objects.filter(aula=aula, fecha__range=(fecha_inicio, fecha_fin), activo=activo, hora_inicio__range=(hora_inicio,hora_fin))
        else:
            practicas = Practica.objects.filter(aula=aula, fecha__range=(fecha_inicio, fecha_fin), activo=activo)

        aulas = Aula.get_active.filter(id=aula.id)

    aula_list=[]
    total_count = 0
    for aula in aulas:
        aula_dict={}
        aula_dict['aula'] = aula
        practicas_aula = practicas.filter(aula=aula)
        aula_dict['practicas'] = practicas_aula 
        aula_dict['count'] = practicas_aula.count()
        total_count+=aula_dict['count']
        aula_list.append(aula_dict)

        
    return render_to_response('reporte_practicas.html', {'titulo':titulo, 'aula_list':aula_list, 'total_count':total_count}, RequestContext(request))

def reporte_informes(request):
    titulo = "Reporte de Informes"
    if request.POST:
        f = RepInformeForm(request.POST)
        if f.errors:
            return render_to_response('f_reporte.html', {'form':f, 'titulo':titulo}, RequestContext(request))        
        else:
            aula = f.cleaned_data['aula']
            fecha_incio = f.cleaned_data['fecha_inicio']
            fecha_fin = f.cleaned_data['fecha_fin']
            tipo = f.cleaned_data['tipo']
            estado = f.cleaned_data['estado']
            return reporte_informes_core(request, aula, fecha_incio, fecha_fin, tipo, estado, titulo = titulo)
    else:
        f = RepInformeForm()
        return render_to_response('f_reporte.html', {'form':f, 'titulo':titulo}, RequestContext(request))


def reporte_informes_core(request, aula, fecha_inicio, fecha_fin, tipo, estado, titulo=""):
    if aula == None:
        informes = Informe.objects.filter(fecha_creacion__range=(fecha_inicio, fecha_fin))
        aulas = Aula.get_active.all()
    else:
        informes = Informe.objects.filter(equipo__aula=aula, fecha_creacion__range=(fecha_inicio, fecha_fin))
        aulas = Aula.get_active.filter(id=aula.id)

    if tipo != "0":
        informes = informes.filter(tipo = tipo)

    if estado != "0":
        informes = informes.filter(estado = estado)


    aula_list=[]
    total_count = 0
    for aula in aulas:
        aula_dict={}
        aula_dict['aula'] = aula
        informes_aula = informes.filter(equipo__aula=aula)
        aula_dict['informes'] = informes_aula 
        aula_dict['count'] = informes_aula.count()
        total_count+=aula_dict['count']
        aula_list.append(aula_dict)

        
    return render_to_response('reporte_informes.html', {'titulo':titulo, 'aula_list':aula_list, 'total_count':total_count}, RequestContext(request))
    

def reporte_inventario(request):
    titulo = "Reporte de Inventario"
    if request.POST:
        f = AulaForm(request.POST)
        if f.errors:
            return render_to_response('f_reporte.html', {'form':f, 'titulo':titulo}, RequestContext(request))        
        else:
            aula = f.cleaned_data['aula']
            total_equipos = 0
            if aula == None:
                aulas = Aula.get_active.all()
            else:
                aulas = Aula.get_active.filter(id=aula.id)
            aula_list = []
            for aula in aulas:
                aula_dict={}
                equipos_aula = aula.equipo_set.filter(activo=1)
                aula_dict['aula'] = aula
                aula_dict['equipos'] = equipos_aula
                aula_dict['count'] = equipos_aula.count()
                total_equipos+=aula_dict['count']
                aula_list.append(aula_dict)
            return render_to_response('reporte_inventario.html', {'aula_list':aula_list,'titulo':titulo, 'total_count':total_equipos}, RequestContext(request))
    else:
        f = AulaForm()
        return render_to_response('f_reporte.html', {'form':f, 'titulo':titulo}, RequestContext(request))


