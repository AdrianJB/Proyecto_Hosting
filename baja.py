# ­*­ coding: utf­8 ­*­

import sys
import os

#Pedimos nombre de usuario y dominio
usuario=sys.argv[1]
dominio=sys.argv[2]

#Comprobamos que existe
if os.path.isdir("/var/www/%s" % (usuario)) == True and os.path.isfile("/etc/apache2/sites-available/%s" % (dominio)) == True:
	os.system("rm -r /var/www/%s" % (usuario))
else:
	print "El usuario o el dominio no existen, introduzca otro usuario y dominio por favor." % (usuario)
	exit()

#Borramos el virtualhost
os.system("a2dissite %s" % (dominio))
os.system("rm /etc/apache2/sites-available/%s" % (dominio))

#Borramos la zona
os.system("sed '/zone " + '"%s"'% (dominio) + "/,/};/d' /etc/bind/named.conf.local > temporal")
os.system("mv temporal /etc/bind/named.conf.local")
os.system("rm /var/cache/bind/db.%s" % (dominio))