from django.db import models
from aulas.models import Equipo
# Create your models here.
TIPOS_INFORME = ((1,"Hardware"),(2,"Software"))
ESTADOS_INFORME = ((1,"Pendiente"),(2,"Arreglado"),(3,"No se arreglara"))

class Informe(models.Model):
    equipo = models.ForeignKey(Equipo)
    descripcion = models.TextField()
    tipo = models.IntegerField(choices = TIPOS_INFORME)
    estado = models.IntegerField(choices = ESTADOS_INFORME, default=1)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    

    #TODO save signal que mande un correo electronico al responsable???
    def get_label_class(self):
        if self.estado == 1:
            return "label-important"
        elif self.estado == 2:
            return "label-success"
        if self.estado == 3:
            return "label-warning"

