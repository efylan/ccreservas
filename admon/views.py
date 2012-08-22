# coding: latin1

from django.shortcuts import render_to_response, HttpResponseRedirect
from django.template import RequestContext
from aulas.models import Aula, Aplicacion, Equipo
from reservaciones.models import Carrera, Alumno, Docente
from admon.forms import AulaForm, EquipoForm, AppForm, CarreraForm, AlumnoForm, DocenteForm, GroupForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, SetPasswordForm
from django.contrib.auth.models import User, Group, Permission
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

from django.contrib.auth.decorators import permission_required


def related_objects_info(obj):
    links = [rel.get_accessor_name() for rel in obj._meta.get_all_related_objects()]

    for link in links:
        objects = getattr(obj, link).all()
        return objects


def home(request):
    return render_to_response('admon_index.html', {}, RequestContext(request))

#----------------------------------------------------

@permission_required('aulas.add_aula', login_url="/login/")
def aula_create(request):
    if request.POST:
        f = AulaForm(request.POST)
        if f.errors:
            messages.error(request, 'El formulario contiene errores.')
            return render_to_response('aulas/create.html', {'form':f}, RequestContext(request))            
        else:
            f.save()
            messages.success(request, 'Aula agregada exitosamente.')
            if 'add_another' in request.POST.keys():
                return HttpResponseRedirect('/administracion/aulas/crear/')
            else:
                return HttpResponseRedirect('/administracion/aulas/')
    else:
        f = AulaForm()    
        return render_to_response('aulas/create.html', {'form':f}, RequestContext(request))

@permission_required('aulas.change_aula', login_url="/login/")
def aula_modify(request, aula_id):
    try:
        aula = Aula.objects.get(id=aula_id)
    except Aula.DoesNotExist:
        messages.error(request, 'Aula no existente.')
        return HttpResponseRedirect('/administracion/aulas/')

    if request.POST:
        f = AulaForm(request.POST, instance = aula)
        if f.errors:
            return render_to_response('aulas/modify.html', {'form':f}, RequestContext(request))
        else:
            f.save()
            messages.success(request, 'Aula editada exitosamente.')
            if 'add_another' in request.POST.keys():
                return HttpResponseRedirect('/administracion/aulas/crear/')
            return HttpResponseRedirect('/administracion/aulas/')

    else:
        f = AulaForm(instance = aula)
        return render_to_response('aulas/modify.html', {'form':f, 'aula':aula}, RequestContext(request))

@permission_required('aulas.delete_aula', login_url="/login/")
def aula_warning(request, aula_id):
    try:
        aula = Aula.objects.get(id=aula_id)
    except Aula.DoesNotExist:
        messages.error(request, 'Aula no existente.')
        return HttpResponseRedirect('/administracion/aulas/')

    if request.POST:
        aula.delete()
        messages.warning(request, 'Aula eliminada exitosamente.')
        return HttpResponseRedirect('/administracion/aulas/')

    related = related_objects_info(aula)

    return render_to_response('aulas/delete.html', {'obj':aula, 'related':related}, RequestContext(request))

def aula_list(request):
    aulas = Aula.get_active.all()
    return render_to_response('aulas/list.html', {'obj_list':aulas}, RequestContext(request))


#----------------------------------------------------

@permission_required('aulas.add_equipo', login_url="/login/")
def equipo_create(request):
    if request.POST:
        f = EquipoForm(request.POST)
        if f.errors:
            messages.error(request, 'El formulario contiene errores.')
            return render_to_response('equipos/create.html', {'form':f}, RequestContext(request))
        else:
            f.save()
            messages.success(request, 'Equipo agregada exitosamente.')
            if 'add_another' in request.POST.keys():
                return HttpResponseRedirect('/administracion/equipos/crear/')
            return HttpResponseRedirect('/administracion/equipos/')
    else:
        f = EquipoForm()    
    return render_to_response('equipos/create.html', {'form':f}, RequestContext(request))

@permission_required('aulas.change_equipo', login_url="/login/")
def equipo_modify(request, equipo_id):
    try:
        equipo = Equipo.objects.get(id=equipo_id)
    except Equipo.DoesNotExist:
        messages.error(request, 'Equipo no existente.')
        return HttpResponseRedirect('/administracion/equipos/')

    if request.POST:
        f = EquipoForm(request.POST, instance = equipo)
        if f.errors:
            return render_to_response('equipos/modify.html', {'form':f}, RequestContext(request))
        else:
            f.save()
            if 'add_another' in request.POST.keys():
                return HttpResponseRedirect('/administracion/equipos/crear/')
            messages.success(request, 'Equipo editado exitosamente.')
            return HttpResponseRedirect('/administracion/equipos/')

    else:
        f = EquipoForm(instance = equipo)
        return render_to_response('equipos/modify.html', {'form':f, 'obj':equipo}, RequestContext(request))

@permission_required('aulas.delete_equipo', login_url="/login/")
def equipo_warning(request, equipo_id):
    try:
        equipo = Equipo.objects.get(id=equipo_id)
    except Equipo.DoesNotExist:
        messages.error(request, 'Equipo no existente.')

    if request.POST:
        equipo.delete()
        messages.warning(request, 'Equipo eliminada exitosamente.')
        return HttpResponseRedirect('/administracion/equipos/')

    return render_to_response('equipos/delete.html', {'obj':equipo}, RequestContext(request))

def equipo_list(request):
    equipos = Equipo.get_active.all()
    return render_to_response('equipos/list.html', {'obj_list':equipos}, RequestContext(request))


#----------------------------------------------------
@permission_required('aulas.add_aplicacion', login_url="/login/")
def app_create(request):
    if request.POST:
        f = AppForm(request.POST)
        if f.errors:
            messages.error(request, 'El formulario contiene errores.')
            return render_to_response('apps/create.html', {'form':f}, RequestContext(request))
        else:
            f.save()
            messages.success(request, 'Aplicacion agregada exitosamente.')
            if 'add_another' in request.POST.keys():
                return HttpResponseRedirect('/administracion/aplicaciones/crear/')
            return HttpResponseRedirect('/administracion/aplicaciones/')
    else:
        f = AppForm()    
    return render_to_response('apps/create.html', {'form':f}, RequestContext(request))

@permission_required('aulas.change_aplicacion', login_url="/login/")
def app_modify(request, app_id):
    try:
        app = Aplicacion.objects.get(id=app_id)
    except Aplicacion.DoesNotExist:
        messages.error(request, 'Aplicacion no existente.')
        return HttpResponseRedirect('/administracion/aplicaciones/')

    if request.POST:
        f = AppForm(request.POST, instance = app)
        if f.errors:
            return render_to_response('apps/modify.html', {'form':f}, RequestContext(request))
        else:
            f.save()
            messages.success(request, 'Aplicacion editada exitosamente.')
            if 'add_another' in request.POST.keys():
                return HttpResponseRedirect('/administracion/aplicaciones/crear/')
            return HttpResponseRedirect('/administracion/aplicaciones/')

    else:
        f = AppForm(instance = app)
        return render_to_response('apps/modify.html', {'form':f, 'obj':app}, RequestContext(request))

@permission_required('aulas.delete_aplicacion', login_url="/login/")
def app_warning(request, app_id):
    try:
        app = Aplicacion.objects.get(id=app_id)
    except Aplicacion.DoesNotExist:
        messages.error(request, 'Aplicacion no existente.')

    if request.POST:
        app.delete()
        messages.warning(request, 'Aplicacion eliminada exitosamente.')
        return HttpResponseRedirect('/administracion/aplicaciones/')

    return render_to_response('apps/delete.html', {'obj':app}, RequestContext(request))


def app_list(request):
    apps = Aplicacion.get_active.all()
    return render_to_response('apps/list.html', {'obj_list':apps}, RequestContext(request))


#----------------------------------------------------

@permission_required('reservaciones.add_carrera', login_url="/login/")
def carrera_create(request):
    if request.POST:
        f = CarreraForm(request.POST)
        if f.errors:
            messages.error(request, 'El formulario contiene errores.')
            return render_to_response('carreras/create.html', {'form':f}, RequestContext(request))
        else:
            f.save()
            messages.success(request, 'Carrera agregada exitosamente.')
            if 'add_another' in request.POST.keys():
                return HttpResponseRedirect('/administracion/carreras/crear/')
            return HttpResponseRedirect('/administracion/carreras/')
    else:
        f = CarreraForm()    
    return render_to_response('carreras/create.html', {'form':f}, RequestContext(request))

@permission_required('reservaciones.change_carrera', login_url="/login/")
def carrera_modify(request, carrera_id):
    try:
        carrera = Carrera.objects.get(id=carrera_id)
    except Carrera.DoesNotExist:
        messages.error(request, 'Carrera no existente.')
        return HttpResponseRedirect('/administracion/carreras/')

    if request.POST:
        f = CarreraForm(request.POST, instance = carrera)
        if f.errors:
            return render_to_response('carreras/modify.html', {'form':f}, RequestContext(request))
        else:
            f.save()
            messages.success(request, 'Carrera editada exitosamente.')
            if 'add_another' in request.POST.keys():
                return HttpResponseRedirect('/administracion/carreras/crear/')
            return HttpResponseRedirect('/administracion/carreras/')

    else:
        f = CarreraForm(instance = carrera)
        return render_to_response('carreras/modify.html', {'form':f, 'obj':carrera}, RequestContext(request))

@permission_required('reservaciones.delete_carrera', login_url="/login/")
def carrera_warning(request, carrera_id):
    try:
        carrera = Carrera.objects.get(id=carrera_id)
    except Carrera.DoesNotExist:
        messages.error(request, 'Carrera no existente.')

    if request.POST:
        carrera.delete()
        messages.warning(request, 'Carrera eliminada exitosamente.')
        return HttpResponseRedirect('/administracion/carreras/')

    return render_to_response('carreras/delete.html', {'obj':carrera}, RequestContext(request))


def carrera_list(request):
    carreras = Carrera.get_active.all()
    return render_to_response('carreras/list.html', {'obj_list':carreras}, RequestContext(request))

#--------------------------------------------

@permission_required('reservaciones.add_alumno', login_url="/login/")
def alumno_create(request):
    if request.POST:
        f = AlumnoForm(request.POST)
        if f.errors:
            messages.error(request, 'El formulario contiene errores.')
            return render_to_response('alumnos/create.html', {'form':f}, RequestContext(request))
        else:
            f.save()
            messages.success(request, 'Alumno agregado exitosamente.')
            if 'add_another' in request.POST.keys():
                return HttpResponseRedirect('/administracion/alumnos/crear/')
            return HttpResponseRedirect('/administracion/alumnos/')
    else:
        f = AlumnoForm()    
    return render_to_response('alumnos/create.html', {'form':f}, RequestContext(request))

@permission_required('reservaciones.change_alumno', login_url="/login/")
def alumno_modify(request, alumno_id):
    try:
        alumno = Alumno.objects.get(pk=alumno_id)
    except Alumno.DoesNotExist:
        messages.error(request, 'Alumno no existente.')
        return HttpResponseRedirect('/administracion/alumnos/')

    if request.POST:
        f = AlumnoForm(request.POST, instance = alumno)
        if f.errors:
            return render_to_response('alumnos/modify.html', {'form':f}, RequestContext(request))
        else:
            f.save()
            messages.success(request, 'Alumno editado exitosamente.')
            if 'add_another' in request.POST.keys():
                return HttpResponseRedirect('/administracion/alumnos/crear/')
            return HttpResponseRedirect('/administracion/alumnos/')

    else:
        f = AlumnoForm(instance = alumno)
        return render_to_response('alumnos/modify.html', {'form':f, 'obj':alumno}, RequestContext(request))

@permission_required('reservaciones.delete_alumno', login_url="/login/")
def alumno_warning(request, alumno_id):
    try:
        alumno = Alumno.objects.get(pk=alumno_id)
    except Alumno.DoesNotExist:
        messages.error(request, 'Alumno no existente.')

    if request.POST:
        alumno.delete()
        messages.warning(request, 'Alumno eliminado exitosamente.')
        return HttpResponseRedirect('/administracion/alumnos/')

    return render_to_response('alumnos/delete.html', {'obj':alumno}, RequestContext(request))


def alumno_list(request):
    alumnos = Alumno.objects.all()
    return render_to_response('alumnos/list.html', {'obj_list':alumnos}, RequestContext(request))

#-------------------------------------------

@permission_required('reservaciones.add_docente', login_url="/login/")
def docente_create(request):
    if request.POST:
        f = DocenteForm(request.POST)
        if f.errors:
            messages.error(request, 'El formulario contiene errores.')
            return render_to_response('docentes/create.html', {'form':f}, RequestContext(request))
        else:
            f.save()
            messages.success(request, 'Docente agregado exitosamente.')
            if 'add_another' in request.POST.keys():
                return HttpResponseRedirect('/administracion/docentes/crear/')
            return HttpResponseRedirect('/administracion/docentes/')
    else:
        f = DocenteForm()    
    return render_to_response('docentes/create.html', {'form':f}, RequestContext(request))

@permission_required('reservaciones.change_docente', login_url="/login/")
def docente_modify(request, docente_id):
    try:
        docente = Docente.objects.get(pk=docente_id)
    except Docente.DoesNotExist:
        messages.error(request, 'Docente no existente.')
        return HttpResponseRedirect('/administracion/docentes/')

    if request.POST:
        f = DocenteForm(request.POST, instance = docente)
        if f.errors:
            return render_to_response('docentes/modify.html', {'form':f}, RequestContext(request))
        else:
            f.save()
            messages.success(request, 'Docente editado exitosamente.')
            if 'add_another' in request.POST.keys():
                return HttpResponseRedirect('/administracion/docentes/crear/')
            return HttpResponseRedirect('/administracion/docentes/')

    else:
        f = DocenteForm(instance = docente)
        return render_to_response('docentes/modify.html', {'form':f, 'obj':docente}, RequestContext(request))

@permission_required('reservaciones.delete_docente', login_url="/login/")
def docente_warning(request, docente_id):
    try:
        docente = Docente.objects.get(pk=docente_id)
    except Docente.DoesNotExist:
        messages.error(request, 'Docente no existente.')

    if request.POST:
        docente.delete()
        messages.warning(request, 'Docente eliminada exitosamente.')
        return HttpResponseRedirect('/administracion/docentes/')

    return render_to_response('docentes/delete.html', {'obj':docente}, RequestContext(request))


def docente_list(request):
    docentes = Docente.objects.all()
    return render_to_response('docentes/list.html', {'obj_list':docentes}, RequestContext(request))



#-------------------------------------------

@permission_required('auth.add_user', login_url="/login/")
def user_create(request):
    if request.POST:
        f = UserCreationForm(request.POST)
        if f.errors:
            messages.error(request, 'El formulario contiene errores.')
            return render_to_response('users/create.html', {'form':f}, RequestContext(request))
        else:
            user = f.save()
            messages.success(request, 'Usuario agregado exitosamente.')
            if 'add_another' in request.POST.keys():
                return HttpResponseRedirect('/administracion/users/editar/%s/' % user.id)
            return HttpResponseRedirect('/administracion/users/editar/%s/' % user.id)
    else:
        f = UserCreationForm()    
    return render_to_response('users/create.html', {'form':f}, RequestContext(request))

@permission_required('auth.change_user', login_url="/login/")
def user_modify(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        messages.error(request, 'Usuario no existente.')
        return HttpResponseRedirect('/administracion/users/')

    if request.POST:
        f = UserChangeForm(request.POST, instance = user)
        if f.errors:
            return render_to_response('users/modify.html', {'form':f}, RequestContext(request))
        else:
            f.save()
            messages.success(request, 'Usuario editado exitosamente.')
            if 'add_another' in request.POST.keys():
                return HttpResponseRedirect('/administracion/users/crear/')
            return HttpResponseRedirect('/administracion/users/')

    else:
        f = UserChangeForm(instance = user)
        return render_to_response('users/modify.html', {'form':f, 'obj':user}, RequestContext(request))

@permission_required('auth.change_user', login_url="/login/")
def user_password(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        messages.error(request, 'Usuario no existente.')
        return HttpResponseRedirect('/administracion/users/')

    if request.POST:
        f = SetPasswordForm(data = request.POST, user = user)
        if f.errors:
            return render_to_response('users/password.html', {'form':f}, RequestContext(request))
        else:
            f.save()
            messages.success(request, 'Contraseña cambiada exitosamente.')
            if 'add_another' in request.POST.keys():
                return HttpResponseRedirect('/administracion/users/crear/')
            return HttpResponseRedirect('/administracion/users/')

    else:
        f = SetPasswordForm(user = user)
        return render_to_response('users/password.html', {'form':f, 'obj':user}, RequestContext(request))

@permission_required('auth.delete_user', login_url="/login/")
def user_warning(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        messages.error(request, 'Usuario no existente.')

    if request.POST:
        user.delete()
        messages.warning(request, 'Usuario eliminado exitosamente.')
        return HttpResponseRedirect('/administracion/users/')

    return render_to_response('users/delete.html', {'obj':user}, RequestContext(request))


def user_list(request):
    users = User.objects.all()
    return render_to_response('users/list.html', {'obj_list':users}, RequestContext(request))


#----------------------------------------
@permission_required('auth.add_group', login_url="/login/")
def group_create(request):
    if request.POST:
        f = GroupForm(request.POST)
        if f.errors:
            messages.error(request, 'El formulario contiene errores.')
            return render_to_response('groups/create.html', {'form':f}, RequestContext(request))
        else:
            f.save()
            messages.success(request, 'Grupo agregado exitosamente.')
            if 'add_another' in request.POST.keys():
                return HttpResponseRedirect('/administracion/groups/crear/')
            return HttpResponseRedirect('/administracion/groups/')
    else:
        f = GroupForm()    
    return render_to_response('groups/create.html', {'form':f}, RequestContext(request))

@permission_required('auth.change_group', login_url="/login/")
def group_modify(request, group_id):
    try:
        group = Group.objects.get(id=group_id)
    except Group.DoesNotExist:
        messages.error(request, 'Grupo no existente.')
        return HttpResponseRedirect('/administracion/groups/')

    if request.POST:
        f = GroupForm(request.POST, instance = group)
        if f.errors:
            return render_to_response('groups/modify.html', {'form':f}, RequestContext(request))
        else:
            f.save()
            messages.success(request, 'Grupo editado exitosamente.')
            if 'add_another' in request.POST.keys():
                return HttpResponseRedirect('/administracion/groups/crear/')
            return HttpResponseRedirect('/administracion/groups/')

    else:
        f = GroupForm(instance = group)
        return render_to_response('groups/modify.html', {'form':f, 'obj':group}, RequestContext(request))

@permission_required('auth.delete_group', login_url="/login/")
def group_warning(request, group_id):
    try:
        group = Group.objects.get(id=group_id)
    except Group.DoesNotExist:
        messages.error(request, 'Grupo no existente.')

    if request.POST:
        group.delete()
        return HttpResponseRedirect('/administracion/groups/')

    return render_to_response('groups/delete.html', {'obj':group}, RequestContext(request))


def group_list(request):
    groups = Group.objects.all()
    return render_to_response('groups/list.html', {'obj_list':groups}, RequestContext(request))

