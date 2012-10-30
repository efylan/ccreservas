#coding: latin1
from django import forms
from reservaciones.models import Reservacion, Practica, Docente
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
    no_empleado=forms.ChoiceField(choices=Docente.objects.all().values_list('no_empleado','nombre'), required=False, label="Número de Tarjeta", help_text="Ingresar cualquiera de")
    rfc=forms.ChoiceField(choices=Docente.objects.all().values_list('rfc','nombre'), required=False)
    class Meta:
        model=Practica
        exclude=('aula')
        fields=('nombre','no_empleado','rfc','no_alumnos','fecha','tipo','hora_inicio','hora_fin')
    def __init__(self, aula, *args, **kwargs):
        super(PracticaForm, self).__init__(*args, **kwargs)
        clase = aula.get_clase_actual()

        self.fields['rfc'].label="RFC docente"
        self.fields['rfc'].widget=forms.TextInput()
        self.fields['rfc'].widget.attrs['id']="id_docente"
        self.fields['rfc'].required=False
        self.fields['rfc'].help_text="los dos datos."

        self.fields['no_empleado'].widget=forms.TextInput()


        if clase:
            self.fields['fecha'].initial= datetime.date.today()
            self.fields['hora_inicio'].initial= clase.hora_inicio
            self.fields['hora_fin'].initial= clase.hora_fin
            self.fields['rfc'].initial=clase.docente.rfc
            self.fields['no_empleado'].initial=clase.docente.no_empleado

        else:
            self.fields['fecha'].initial= datetime.date.today()
            self.fields['hora_inicio'].initial= get_now_start(redondear=True)
            self.fields['hora_fin'].initial= get_now_end()

    def clean_rfc(self):
        if 'rfc' in self.cleaned_data:
            rfc = self.cleaned_data['rfc']
        else:
            rfc=''

        if 'no_empleado' in self.cleaned_data:
            num = self.cleaned_data['no_empleado']
        else:
            num=''

        if len(rfc) > 0 or len(num) > 0:
            return self.cleaned_data['rfc']
        else:
            raise forms.ValidationError("Por favor ingresar RFC o Número de Empleado")
            return self.cleaned_data['rfc']

