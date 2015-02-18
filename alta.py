# ­*­ coding: utf­8 ­*­

import sys
import os

#Pedimos nombre de usuario y dominio
usuario=sys.argv[1]
dominio=sys.argv[2]

#Comprobamos que no existen y creamos la carpeta si es asi, 
#sino lanzamos error.

if os.path.isdir("/var/www/%s" % usuario) = False
and os.path.isfile("/etc/apache2/sites-available/%s" %dominio) = False:
	os.system("mkdir /var/www/%s" %usuario)
	os.system("touch /etc/apache2/sites-available/%s" %dominio)
else:
	print "El usuario %s ya existe, introduzca otro usuario por favor." % (usuario)
	exit()

#Creamos el virtualhost en apache2
ficherovirtualhost = open("plantillas/virtualhost","r")
lineas3 = ficherovirtualhost.readlines()
ficherovirtualhost.close()
virtualhost = open("/etc/apache2/sites-available/%s" %dominio,"w")
for linea3 in lineas3:
	linea3 = linea3.replace('dominio',dominio)
	virtualhost.write(linea3)
virtualhost.close()
os.system("a2ensite %s" %dominio)
os.system("service apache2 restart")

#1 Verificar usuario y dominio X
#2 Crear la carpeta del usuario X
#	/srv/www/usuario			X
#3 Crear el virtualhost en apache (plantilla) X
#4 Crear usuario ftp
#5 Crear usuario y bd en mysql (Hacer en LDAP)
#6 Zona DNS
#	/etc/bind9/named.conf.local
#	/var/cache/bind9/db.dominio