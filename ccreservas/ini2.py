from aulas.models import *
from reservaciones.models import *
import datetime
import os

readfile = open(os.path.join(os.path.dirname(__file__), 'scheduledump2.txt'),'r')
periodo = Periodo.objects.get(id=1)
counter=0
docente_counter = 1
for line in readfile.readlines():
    print "---------------------"
    data=line.split(',')
    nom_aula = data[0]
    try:
        aula = Aula.objects.get(nombre=nom_aula)
        print nom_aula, " existente"
    except Aula.DoesNotExist:
        print "Creando ",nom_aula
        aula = Aula()
        aula.nombre = nom_aula
        aula.save()
    hr_ini = datetime.time(hour=int(data[1]))
    hr_fin = datetime.time(hour=int(data[2]))
    nom_materia = data[3]
    try:
        materia = Materia.objects.get(nombre=nom_materia)
        print nom_materia, " existente"
    except Materia.DoesNotExist:
        materia = Materia()
        materia.nombre=nom_materia
        materia.clave = str(counter)+nom_materia[0]
        materia.save()
        print "creando ", nom_materia
    nom_docente = data[4]
    ape_p=data[5]
    ape_m=data[6]
    try:
        docente=Docente.objects.get(nombre=nom_docente,apellido_paterno=ape_p,apellido_materno=ape_m)
        print nom_docente, " existente"
    except:
        docente=Docente()
        docente.nombre = nom_docente
        docente.apellido_paterno=ape_p
        docente.apellido_materno=ape_m
        if docente_counter > 9:
           prefix = "0"
        if docente_counter > 99:
           prefix = ""
        if docente_counter < 10:
           prefix = "00"
        docente.rfc="%s%s"%(nom_docente[0],ape_p)
        docente.no_empleado=str(prefix)+str(docente_counter)
        docente.save()
        docente_counter+=1
        print "creando ", nom_docente, ape_p, ape_m
    dias = data[7].split('|')
    print dias
    for dia in dias:
        clase = Clase()
        clase.aula = aula
        clase.dia = int(dia) - 1
        clase.hora_inicio = hr_ini
        clase.hora_fin = hr_fin
        clase.docente = docente
        clase.materia = materia
        clase.periodo = periodo
        clase.tipo = 0
        clase.save()
    print "clase ", counter
    counter+=1

