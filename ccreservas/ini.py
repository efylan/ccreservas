from aulas.models import *

rng = range(0,20)

apps = ['CLIPS', 'Visual Basic .net', "C++", "Java", "Microsoft Access", "Office 2010", "Office 2007", "AutoCAD", "Fireworks", "Flash 11"]

for app in apps:
        try:
                apli  = Aplicacion()
                apli.nombre = app
                apli.save()
        except:
                pass


for aula in Aula.objects.all():
        for r in rng:
                try:
                    equipo=Equipo()
                    equipo.nombre="%s-%s" % (aula.nombre, r)
                    equipo.aula=aula
                    equipo.marca="HP"
                    equipo.modelo="1001"
                    ram=1024
                    equipo.ram=1024
                    equipo.disco_duro=512
                    if aula.nombre=="S5":
                        equipo.sistema_operativo="Ubuntu Linux 12.04"
                        equipo.save()
                    elif aula.nombre=="S4":
                        equipo.sistema_operativo="Windows 7"
                        equipo.save()
                        for app in Aplicacion.objects.all()[0:2]:
                            equipo.aplicaciones.add(app)
                    elif aula.nombre=="S3":
                        equipo.sistema_operativo="Windows XP"
                        equipo.save()
                        for app in Aplicacion.objects.all()[2:5]:
                            equipo.aplicaciones.add(app)
                    elif aula.nombre=="S2":
                        equipo.sistema_operativo="Windows 7"
                        equipo.save()
                        for app in Aplicacion.objects.all()[5:7]:
                            equipo.aplicaciones.add(app)
                    elif aula.nombre=="S1":
                        equipo.sistema_operativo="Windows 7"
                        equipo.save()
                    else:
                        equipo.sistema_operativo="Windows 7"
                        equipo.save()
                        for app in Aplicacion.objects.all()[7:9]:
                            equipo.aplicaciones.add(app)
                except:
                    pass
