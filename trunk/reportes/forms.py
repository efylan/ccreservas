from django import forms
from aulas.models import Aula

TIPO_INF_CHOICES=((0,'Todas las categorias'),(1,'Hardware'),(2,'Software'))
ESTADO_INF_CHOICES=((0,'Todas las condiciones'),(1,'Pendiente'),(2,'Arreglado'),(3,'No se arreglara'))

class AulaFechaForm(forms.Form):
    aula = forms.ModelChoiceField(queryset=Aula.get_active.all(), required=False, empty_label="Todas")
    fecha_inicio = forms.DateField(label = "Desde el dia", help_text="Las fechas son obligatorias.")
    fecha_fin = forms.DateField(label = "Hasta el dia", help_text="Formato: dd/mm/aaaa")
    hora_inicio = forms.TimeField(required=False, help_text="Las horas son opcionales.")
    hora_fin = forms.TimeField(required=False, help_text="Formato de 24 horas ej. 4:00pm es 16:00")

    

class AulaForm(forms.Form):
    aula = forms.ModelChoiceField(queryset=Aula.get_active.all(), required=False, empty_label="Todas")

class RepInformeForm(forms.Form):
    aula = forms.ModelChoiceField(queryset=Aula.get_active.all(), required=False, empty_label="Todas")
    fecha_inicio = forms.DateField(label = "Desde el dia", help_text="Formato: dd/mm/aaaa")
    fecha_fin = forms.DateField(label = "Hasta el dia")
    tipo = forms.ChoiceField(choices=TIPO_INF_CHOICES, label="Categoria")
    estado = forms.ChoiceField(choices=ESTADO_INF_CHOICES, label="Condicion")
