from django.shortcuts import render_to_response, HttpResponseRedirect
from django.template import RequestContext
from django.contrib import messages
from informes.models import Informe
from aulas.models import Equipo
from informes.forms import InformeForm, ResolverForm

def home(request):
    informes = Informe.objects.all().order_by('estado','-fecha_creacion')
    return render_to_response('informes_index.html', {'informes':informes}, RequestContext(request))

def informes_pendientes(request):
    informes = Informe.objects.filter(estado=1).order_by('estado','-fecha_creacion')
    return render_to_response('informes_index.html', {'informes':informes}, RequestContext(request))

def informes_arreglados(request):
    informes = Informe.objects.filter(estado=2).order_by('estado','-fecha_creacion')
    return render_to_response('informes_index.html', {'informes':informes}, RequestContext(request))

def informes_wontfix(request):
    informes = Informe.objects.filter(estado=3).order_by('estado','-fecha_creacion')
    return render_to_response('informes_index.html', {'informes':informes}, RequestContext(request))


def levantar_informe_equipo(request, equipo_id):
    try:
        equipo = Equipo.get_active.get(id=equipo_id)
    except Equipo.DoesNotExist:
        messages.error(request, 'Equipo no existente')
        return HttpResponseRedirect('/reservaciones/')

    if request.POST:
        f = InformeForm(request.POST)
        if f.errors:
            return render_to_response('levantar_informe_equipo.html', {'form':f, 'equipo':equipo}, RequestContext(request))
        else:
            informe = f.save(commit=False)
            informe.equipo=equipo
            informe.save()
            messages.success(request, 'El informe ha sido levantado.')
            return HttpResponseRedirect('/reservaciones/aula/%s/' % equipo.aula.id)
    else:
        f = InformeForm()
        return render_to_response('levantar_informe_equipo.html', {'form':f, 'equipo':equipo}, RequestContext(request))
    
def resolver_informe(request, informe_id):
    try:
        informe = Informe.objects.get(id=informe_id)
    except Informe.DoesNotExist:
        messages.error(request, 'Informe no existente')
        return HttpResponseRedirect('/reservaciones/')

    if request.POST:
        f = ResolverForm(data = request.POST, instance = informe)
        if f.errors:
            return render_to_response('resolver_informe.html', {'form':f, 'informe':informe}, RequestContext(request))
        else:
            informe = f.save()
            messages.info(request, 'El informe ha sido resuelto como %s.' % informe.get_estado_display())
            return HttpResponseRedirect('/informes/')

    else:
        f = ResolverForm(instance = informe)
        return render_to_response('resolver_informe.html', {'form':f, 'informe':informe}, RequestContext(request))
