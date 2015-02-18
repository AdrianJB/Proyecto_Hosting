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
	os.system("mkdir /etc/apache2/sites-available/%s" %dominio)
else:
	print "El usuario %s ya existe, introduzca otro usuario por favor." % (usuario)
