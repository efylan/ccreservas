# coding: latin1

from django.shortcuts import render_to_response, HttpResponseRedirect
from django.template import RequestContext
from aulas.models import Aula, Aplicacion, Equipo
from reservaciones.models import Carrera, Alumno, Docente, Periodo, Materia, Clase
from admon.forms import AulaForm, EquipoForm, AppForm, CarreraForm, AlumnoForm, DocenteForm, GroupForm, PeriodoForm, ClaseForm, MateriaForm
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

#----------------------------------------------------

@permission_required('reservaciones.add_periodo', login_url="/login/")
def periodo_create(request):
    if request.POST:
        f = PeriodoForm(request.POST)
        if f.errors:
            messages.error(request, 'El formulario contiene errores.')
            return render_to_response('periodos/create.html', {'form':f}, RequestContext(request))
        else:
            f.save()
            messages.success(request, 'Periodo agregado exitosamente.')
            if 'add_another' in request.POST.keys():
                return HttpResponseRedirect('/administracion/periodos/crear/')
            return HttpResponseRedirect('/administracion/periodos/')
    else:
        f = PeriodoForm()    
    return render_to_response('periodos/create.html', {'form':f}, RequestContext(request))

@permission_required('reservaciones.change_periodo', login_url="/login/")
def periodo_modify(request, periodo_id):
    try:
        periodo = Periodo.objects.get(id=periodo_id)
    except Periodo.DoesNotExist:
        messages.error(request, 'Periodo no existente.')
        return HttpResponseRedirect('/administracion/periodos/')

    if request.POST:
        f = PeriodoForm(request.POST, instance = periodo)
        if f.errors:
            return render_to_response('periodos/modify.html', {'form':f}, RequestContext(request))
        else:
            f.save()
            messages.success(request, 'Periodo editado exitosamente.')
            if 'add_another' in request.POST.keys():
                return HttpResponseRedirect('/administracion/periodos/crear/')
            return HttpResponseRedirect('/administracion/periodos/')

    else:
        f = PeriodoForm(instance = periodo)
        return render_to_response('periodos/modify.html', {'form':f, 'obj':periodo}, RequestContext(request))

@permission_required('reservaciones.delete_periodo', login_url="/login/")
def periodo_warning(request, periodo_id):
    try:
        periodo = Periodo.objects.get(id=periodo_id)
    except Periodo.DoesNotExist:
        messages.error(request, 'Periodo no existente.')

    if request.POST:
        periodo.delete()
        messages.warning(request, 'Periodo eliminado exitosamente.')
        return HttpResponseRedirect('/administracion/periodos/')

    return render_to_response('periodos/delete.html', {'obj':periodo}, RequestContext(request))


def periodo_list(request):
    periodos = Periodo.objects.all()
    return render_to_response('periodos/list.html', {'obj_list':periodos}, RequestContext(request))

#----------------------------------------------------

@permission_required('reservaciones.add_materia', login_url="/login/")
def materia_create(request):
    if request.POST:
        f = MateriaForm(request.POST)
        if f.errors:
            messages.error(request, 'El formulario contiene errores.')
            return render_to_response('materias/create.html', {'form':f}, RequestContext(request))
        else:
            f.save()
            messages.success(request, 'Materia agregada exitosamente.')
            if 'add_another' in request.POST.keys():
                return HttpResponseRedirect('/administracion/materias/crear/')
            return HttpResponseRedirect('/administracion/materias/')
    else:
        f = MateriaForm()    
    return render_to_response('materias/create.html', {'form':f}, RequestContext(request))

@permission_required('reservaciones.change_materia', login_url="/login/")
def materia_modify(request, materia_id):
    try:
        materia = Materia.objects.get(id=materia_id)
    except Materia.DoesNotExist:
        messages.error(request, 'Materia no existente.')
        return HttpResponseRedirect('/administracion/materias/')

    if request.POST:
        f = MateriaForm(request.POST, instance = materia)
        if f.errors:
            return render_to_response('materias/modify.html', {'form':f}, RequestContext(request))
        else:
            f.save()
            messages.success(request, 'Materia editada exitosamente.')
            if 'add_another' in request.POST.keys():
                return HttpResponseRedirect('/administracion/materias/crear/')
            return HttpResponseRedirect('/administracion/materias/')

    else:
        f = MateriaForm(instance = materia)
        return render_to_response('materias/modify.html', {'form':f, 'obj':materia}, RequestContext(request))

@permission_required('reservaciones.delete_materia', login_url="/login/")
def materia_warning(request, materia_id):
    try:
        materia = Materia.objects.get(id=materia_id)
    except Materia.DoesNotExist:
        messages.error(request, 'Materia no existente.')

    if request.POST:
        materia.delete()
        messages.warning(request, 'Materia eliminada exitosamente.')
        return HttpResponseRedirect('/administracion/materias/')

    return render_to_response('materias/delete.html', {'obj':materia}, RequestContext(request))


def materia_list(request):
    materias = Materia.objects.all()
    return render_to_response('materias/list.html', {'obj_list':materias}, RequestContext(request))

#----------------------------------------------------

@permission_required('reservaciones.add_clase', login_url="/login/")
def clase_create(request):
    if request.POST:
        f = ClaseForm(request.POST)
        if f.errors:
            messages.error(request, 'El formulario contiene errores.')
            return render_to_response('clases/create.html', {'form':f}, RequestContext(request))
        else:
            f.save()
            messages.success(request, 'Clase agregada exitosamente.')
            if 'add_another' in request.POST.keys():
                return HttpResponseRedirect('/administracion/clases/crear/')
            return HttpResponseRedirect('/administracion/clases/')
    else:
        f = ClaseForm()    
    return render_to_response('clases/create.html', {'form':f}, RequestContext(request))

@permission_required('reservaciones.change_clase', login_url="/login/")
def clase_modify(request, clase_id):
    try:
        clase = Clase.objects.get(id=clase_id)
    except Clase.DoesNotExist:
        messages.error(request, 'Clase no existente.')
        return HttpResponseRedirect('/administracion/clases/')

    if request.POST:
        f = ClaseForm(request.POST, instance = clase)
        if f.errors:
            return render_to_response('clases/modify.html', {'form':f}, RequestContext(request))
        else:
            f.save()
            messages.success(request, 'Clase editada exitosamente.')
            if 'add_another' in request.POST.keys():
                return HttpResponseRedirect('/administracion/clases/crear/')
            return HttpResponseRedirect('/administracion/clases/')

    else:
        f = ClaseForm(instance = clase)
        return render_to_response('clases/modify.html', {'form':f, 'obj':clase}, RequestContext(request))

@permission_required('reservaciones.delete_clase', login_url="/login/")
def clase_warning(request, clase_id):
    try:
        clase = Clase.objects.get(id=clase_id)
    except Clase.DoesNotExist:
        messages.error(request, 'Clase no existente.')

    if request.POST:
        clase.delete()
        messages.warning(request, 'Clase eliminada exitosamente.')
        return HttpResponseRedirect('/administracion/clases/')

    return render_to_response('clases/delete.html', {'obj':clase}, RequestContext(request))


def clase_list(request):
    clases = Clase.objects.all()
    return render_to_response('clases/list.html', {'obj_list':clases}, RequestContext(request))

