from django import forms
from reservaciones.models import Reservacion, Practica
import datetime

def get_now_start(redondear=True):
    ahora = datetime.datetime.now().time()
    if redondear==True:
        inicio = datetime.time(hour=ahora.hour)
    else:
        inicio = datetime.time(hour=ahora.hour, minute=ahora.minute)
    return inicio

def get_now_end():
    ahora = datetime.datetime.now()
    delta = datetime.timedelta(hours=1)
    fecha_fin = ahora + delta
    fin = datetime.time(hour=fecha_fin.hour)
    return fin

class AhoraEquipoForm(forms.ModelForm):
    class Meta:
        model=Reservacion
        exclude=('equipo','hora_inicio','hora_fin','fecha')

class ResEquipoForm(forms.ModelForm):
    class Meta:
        model=Reservacion
        exclude=('equipo')
    def __init__(self, *args, **kwargs):
        super(ResEquipoForm, self).__init__(*args, **kwargs)
        self.fields['fecha'].initial= datetime.date.today()
        self.fields['hora_inicio'].initial= get_now_start(redondear=False)
        self.fields['hora_fin'].initial= get_now_end()
        self.fields['alumno'].widget=forms.TextInput()

class PracticaForm(forms.ModelForm):
    class Meta:
        model=Practica
        exclude=('aula')
    def __init__(self, *args, **kwargs):
        super(PracticaForm, self).__init__(*args, **kwargs)
        self.fields['fecha'].initial= datetime.date.today()
        self.fields['hora_inicio'].initial= get_now_start(redondear=False)
        self.fields['hora_fin'].initial= get_now_end()
        self.fields['docente'].label="RFC docente"
        self.fields['docente'].widget=forms.TextInput()

