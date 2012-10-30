from django.db import models
from django.db.models import Q
import datetime
# Create your models here.
class AulaActivesManager(models.Manager):
    def get_query_set(self):
        return super(AulaActivesManager, self).get_query_set().filter(activo=1)

class Aula(models.Model):
    nombre = models.CharField(max_length=5, help_text="Nombre del Aula", unique=True)
    activo = models.BooleanField(default=1, editable=False)
    get_active = AulaActivesManager()
    objects = models.Manager()

    def __unicode__(self):
        return self.nombre

    def disponible(self, fecha=None, ini=None, fin=None):
        now = datetime.datetime.now()
        if fecha == None:
            fecha = now.date()
        if ini == None:
            ini = now.time()
        if fin == None:
            fin = now.time()

        practicas = self.practica_set.filter(Q(fecha=fecha) & Q(hora_inicio__lte=ini) & Q(hora_fin__gte=fin) & Q(activo=1)).count()
        print practicas
        if practicas > 0:
            return False
        else:
            return True

    def get_disponibles_count(self, fecha=None, hora=None):
        now = datetime.datetime.now()
        if fecha == None:
            fecha = now.date()
        if hora == None:
            hora = now.time()
        equipos = self.equipo_set.all()
        
        reservados = equipos.filter(Q(reservacion__fecha=fecha) & Q(reservacion__hora_inicio__lte=hora) & Q(reservacion__hora_fin__gte=hora) & Q(reservacion__activo=1)).count()

        disponibles = equipos.count() - reservados
        if not self.disponible(now.date(), now.time(), now.time()):
            disponibles = 0

        return disponibles

    def total_equipos(self):
        return self.equipo_set.filter(activo=1).count()

    def get_practica_actual(self, fecha=None, ini=None, fin=None):
        now = datetime.datetime.now()
        if fecha == None:
            fecha = now.date()
        if ini == None:
            ini = now.time()
        if fin == None:
            fin = now.time()

        practicas = self.practica_set.filter(Q(fecha=fecha) & Q(hora_inicio__lte=ini) & Q(hora_fin__gte=fin) & Q(activo=1))

        if practicas.count() > 0:
            return practicas[0]
        else:
            return False

    def get_clase_actual(self, fecha=None, ini=None, fin=None):
        now = datetime.datetime.now()
        if fecha == None:
            fecha = now.date()
        if ini == None:
            ini = now.time()
        if fin == None:
            fin = now.time()

        weekday = now.weekday()
        
        clases = self.clase_set.filter(Q(dia=weekday) & Q(hora_inicio__lte=ini) & Q(hora_fin__gte=fin) & Q(periodo__fecha_inicio__lte=now.date()) & Q(periodo__fecha_fin__gte=now.date()))

        if clases.count() > 0:
            return clases[0]
        else:
            return False


class AppActivesManager(models.Manager):
    def get_query_set(self):
        return super(AppActivesManager, self).get_query_set().filter(activo=1)

class Aplicacion(models.Model):
    nombre = models.CharField(max_length=75, unique=True)
    activo = models.BooleanField(default=1, editable=False)
    get_active = AppActivesManager()
    objects = models.Manager()

    def __unicode__(self):
        return self.nombre

class EquipoActivesManager(models.Manager):
    def get_query_set(self):
        return super(EquipoActivesManager, self).get_query_set().filter(activo=1)

class Equipo(models.Model):
    nombre = models.CharField(max_length=20, unique=True)
    aula = models.ForeignKey(Aula)
    marca = models.CharField(max_length=20)
    modelo = models.CharField(max_length=50)
    ram = models.IntegerField(help_text="En Megabytes")
    disco_duro = models.IntegerField(help_text="En Gigabytes")
    sistema_operativo=models.CharField(max_length=30)
    aplicaciones = models.ManyToManyField(Aplicacion, verbose_name="Aplicaciones Instaladas", blank=True)
    activo = models.BooleanField(default = True)
    get_active = EquipoActivesManager()
    objects = models.Manager()

    def __unicode__(self):
        return self.nombre

    def disponible(self, fecha=None, ini=None, fin=None):

        now = datetime.datetime.now()
        if fecha == None:
            fecha = now.date()
        if ini == None:
            ini = now.time()
        if fin == None:
            fin = now.time()

        reservas = self.reservacion_set.filter(Q(fecha=fecha) & Q(hora_inicio__lte=ini) & Q(hora_fin__gte=fin) & Q(activo=1))
        practicas = self.aula.practica_set.filter(Q(fecha=fecha) & Q(hora_inicio__lte=ini) & Q(hora_fin__gte=fin) & Q(activo=1))
        if reservas.count() > 0 or practicas.count() > 0:
            return False
        else:
            return True

    def get_reserva(self, fecha, hr_ini, hr_fin):
        now = datetime.datetime.now().time()
        reservas = self.reservacion_set.filter(Q(fecha=fecha) & Q(hora_inicio__lte=now) & Q(hora_fin__gte=now)&Q(activo=1))
        if reservas.count() > 0:
            return reservas[0]
        else:
            return None
        

    #TODO agregar metodos de estado de reservacion
