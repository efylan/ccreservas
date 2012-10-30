# coding: latin1
from django.db import models
from aulas.models import Equipo, Aula
import datetime
# Create your models here.

WEEKDAYS = ((0,'Lunes'), (1,'Martes'), (2,'Miercoles'), (3,'Jueves'), (4,'Viernes'), (5,'Sabado'), (6,'Domingo'))

TIPO_CLASE_CHOICES = ((0,'Clase'),(1,'Curso'))

# Create your models here.
class CarreraActivesManager(models.Manager):
    def get_query_set(self):
        return super(CarreraActivesManager, self).get_query_set().filter(activo=1)


class Carrera(models.Model): 
    clave = models.CharField(max_length=25, unique=True)
    nombre = models.CharField(max_length=60, unique = True)
    activo = models.BooleanField(default=1, editable=False)
    get_active = CarreraActivesManager()
    objects = models.Manager()

    def __unicode__(self):
        return self.nombre


class Alumno(models.Model):
    num_control = models.CharField(max_length=8, verbose_name="Numero de Control", primary_key=True, unique=True)
    nombre = models.CharField(max_length=50)
    apellido_paterno = models.CharField(max_length=30)
    apellido_materno = models.CharField(max_length=30)
    carrera = models.ForeignKey(Carrera) 

    def __unicode__(self):
        return self.num_control


class Docente(models.Model):
    no_empleado = models.CharField(max_length=5, unique=True, verbose_name="Número de Tarjeta")
    rfc = models.CharField(max_length=13, unique=True, verbose_name="RFC", primary_key=True)
    nombre = models.CharField(max_length=50)
    apellido_paterno = models.CharField(max_length=30)
    apellido_materno = models.CharField(max_length=30)

    def __unicode__(self):
        return "%s - %s %s %s" % (self.rfc, self.apellido_paterno, self.apellido_materno, self.nombre)



class Materia(models.Model):
    clave = models.CharField(max_length=25, unique = True)
    nombre = models.CharField(max_length=75)

    def __unicode__(self):
        return self.nombre


class ReservacionActivesManager(models.Manager):
    def get_query_set(self):
        return super(ReservacionActivesManager, self).get_query_set().filter(activo=1)
    
class Reservacion(models.Model):
    equipo = models.ForeignKey(Equipo)
    alumno = models.ForeignKey(Alumno)
    fecha = models.DateField()
    activo = models.BooleanField(default=1, editable=False)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    get_active = ReservacionActivesManager()
    objects = models.Manager()

class PracticaActivesManager(models.Manager):
    def get_query_set(self):
        return super(PracticaActivesManager, self).get_query_set().filter(activo=1)

class Practica(models.Model):
    aula = models.ForeignKey(Aula)
    nombre = models.CharField(max_length=75, verbose_name="Título de la Práctica")
    docente = models.ForeignKey(Docente)
    #materia = models.ForeignKey(Materia)  ????
    no_alumnos = models.IntegerField(verbose_name="Número de Alumnos")
    fecha = models.DateField()
    tipo = models.IntegerField(choices = TIPO_CLASE_CHOICES, default=0)
    activo = models.BooleanField(default=1,editable=False)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    get_active = PracticaActivesManager()
    objects = models.Manager()

class Periodo(models.Model):
    nombre = models.CharField(max_length=30)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()

    def __unicode__(self):
        return self.nombre

class Clase(models.Model):
    aula = models.ForeignKey(Aula)
    dia = models.IntegerField(choices = WEEKDAYS)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    docente = models.ForeignKey(Docente)
    materia = models.ForeignKey(Materia)
    periodo = models.ForeignKey(Periodo)
    tipo = models.IntegerField(choices = TIPO_CLASE_CHOICES)

    def __unicode__(self):
        return "%s %s %s - %s" % (self.materia, self.get_dia_display(), self.hora_inicio, self.hora_fin)

