# ­*­ coding: utf­8 ­*­

import sys
import os

#Pedimos nombre de usuario y dominio
usuario=sys.argv[1]
dominio=sys.argv[2]

#Comprobamos que no existen y creamos la carpeta si es asi, 
#sino lanzamos error.

if os.path.isdir("/var/www/%s" % (usuario)) == False and os.path.isfile("/etc/apache2/sites-available/%s" % (dominio)) == False:
	os.system("mkdir /var/www/%s" % (usuario))
else:
	print "El usuario o el dominio ya existen, introduzca otro usuario y dominio por favor." % (usuario)
	exit()

#Creamos el virtualhost en apache2
ficherovirtualhost = open("plantillas/virtualhost","r")
lineas = ficherovirtualhost.read()
ficherovirtualhost.close()
virtualhost = open("/etc/apache2/sites-available/%s" % (dominio),"w")
lineas = lineas.replace('**dominio**',dominio)
lineas = lineas.replace('**usuario**',usuario)
virtualhost.write(lineas)
virtualhost.close()
os.system("a2ensite %s" % (dominio))
os.system("service apache2 restart")

#Introducir las zonas nuevas a named.conf.local
linea2 = '\nzone ' +'"' + dominio +'"' +'{\ntype master;\nfile "db.'+ dominio +'"' +';\n}; '
ficheronamed = open("/etc/bind/named.conf.local","a")
ficheronamed.write(linea2)
ficheronamed.close()

#Ficheros de la zona nueva
plantillazonadb = open("plantillas/zonadb","r")
lineas2 = plantillazonadb.read()
plantillazonadb.close()
ficherozonadb = open("/var/cache/bind/db.%s" % (dominio),"w")
lineas2 = lineas2.replace('**dominio**',dominio)
ficherozonadb.write(lineas2)
ficherozonadb.close()

#1 Verificar usuario y dominio X
#2 Crear la carpeta del usuario X
#	/srv/www/usuario			X
#3 Crear el virtualhost en apache (plantilla) X

#4 Crear usuario ftp
#5 Crear usuario y bd en mysql (Hacer en LDAP)

#6 Zona DNS X
#	/etc/bind9/named.conf.local X
#	/var/cache/bind9/db.dominio X