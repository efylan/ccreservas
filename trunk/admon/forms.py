from django import forms
from aulas.models import Aula, Equipo, Aplicacion
from django.contrib.auth.models import Group
from reservaciones.models import Carrera, Alumno, Docente, Periodo, Clase, Materia

class AulaForm(forms.ModelForm):
    class Meta:
        model = Aula

class EquipoForm(forms.ModelForm):
    class Meta:
        model = Equipo

class AppForm(forms.ModelForm):
    class Meta:
        model = Aplicacion

class CarreraForm(forms.ModelForm):
    class Meta:
        model = Carrera

class AlumnoForm(forms.ModelForm):
    class Meta:
        model = Alumno

class DocenteForm(forms.ModelForm):
    class Meta:
        model = Docente

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group

class PeriodoForm(forms.ModelForm):
    class Meta:
        model = Periodo

class ClaseForm(forms.ModelForm):
    class Meta:
        model = Clase

class MateriaForm(forms.ModelForm):
    class Meta:
        model = Materia

