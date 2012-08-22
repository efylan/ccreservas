from django import forms
from informes.models import Informe

class InformeForm(forms.ModelForm):
    class Meta:
        model=Informe
        exclude=("equipo", "estado")

class ResolverForm(forms.ModelForm):
    class Meta:
        model=Informe
        exclude=("equipo", "tipo", "descripcion")

