from aulas.models import *
import datetime
import os

#TODO*aula
#TODO*aplicaciones

readfile = open('/home/efylan/Desktop/Inventario/s1.csv','r')

apps = Aplicacion.objects.none()
equipos = Equipo.objects.none()
for line in readfile.readlines():
    data=line.split(',')
    if data[0] == "AULA":
        try:
            aula = Aula.objects.get(nombre = data[1])
        except:
            aula = Aula()
            aula.nombre = data[1]
        for equipo in equipos:
            equipo.aplicaciones.add(apps)
        equipos = Equipo.objects.none()
        apps = Aplicacion.objects.none()
        print"----------------------------------------"
        print"-------------------%s-------------------" % aula.nombre
        print"----------------------------------------"
    else:
        pass


    if data[0] == "SW":
        app = Aplicacion.objects.filter(nombre=data[1].upper())
        if app.count() > 0:            
            apps = apps | app
        else:
            n_app = Aplicacion()
            n_app.nombre = data[1].upper()
            n_app.save()
            app = Aplicacion.objects.filter(nombre=n_app.nombre)
            apps = apps | app
        print app
    else:
        pass

    if data[2] == "CPU":
        equipo = Equipo()
        if int(data[0]) < 10:
            prefix = "00"
        else:
            prefix="0"
        equipo.nombre = "CC"+aula.nombre+prefix+data[0]
        equipo.marca = data[1]
        equipo.modelo = data[3]
        raw_ram=data[6].split(" ")[0]
        ram = float(raw_ram)*1024
        equipo.ram = ram
        raw_hdd=data[7].split(" ")[0]
        hdd = float(raw_hdd)
        equipo.disco_duro = hdd
        equipo.sistema_operativo = data[8]
    elif data[2] == "TECLADO":
        pass
    elif data[2] == "MOUSE":
        equipo.sistema_operativo = equipo.sistema_operativo+ " " + data[8]
    elif data[2] == "MONITOR":
        try:
            equipo.aula = aula
            equipo.save()
            print equipo.nombre, " Creado"
        except:
            print equipo.nombre, " Existente"
    else:
        pass
