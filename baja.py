# ­*­ coding: utf­8 ­*­

import sys
import os
import MySQLdb

#Pedimos nombre de usuario y dominio
usuario=sys.argv[1]
dominio=sys.argv[2]

#Comprobamos que existe
if os.path.isdir("/var/www/%s" % (usuario)) == True and os.path.isfile("/etc/apache2/sites-available/%s" % (dominio)) == True:
	os.system("rm -r /var/www/%s" % (usuario))
else:
	print "El usuario %s o el dominio no existen, introduzca otro usuario y dominio por favor." % (usuario)
	exit()

#Borramos el virtualhost
os.system("a2dissite %s>/dev/null" % (dominio))
os.system("rm /etc/apache2/sites-available/%s" % (dominio))
#Borramos el virtualhost para mysql
os.system("a2dissite mysql_%s>/dev/null" % (dominio))
os.system("rm /etc/apache2/sites-available/mysql_%s" % (dominio))
#Reiniciamos apache2
os.system("service apache2 restart>/dev/null")

#Abrimos una conexion con la base de datos que contiene los usuarios virtuales
base = MySQLdb.connect(host="localhost", user="root", passwd="usuario", db="ftp")
cursor=base.cursor()

#Borramos el usuario en mysql y su base de datos
borrarbd="drop database %s" % (usuario)
cursor.execute(borrarbd)
base.commit()
borrausu=" drop user my%s@localhost" % (usuario)
cursor.execute(borrausu)
base.commit()
#Borramos el usuario para ftp
borrarcol="delete from usuarios where ndominio='%s';" % (dominio)
cursor.execute(borrarcol)
base.commit()
base.close()

#Borramos la zona
os.system("sed '/zone " + '"%s"'% (dominio) + "/,/};/d' /etc/bind/named.conf.local > temporal")
os.system("mv temporal /etc/bind/named.conf.local")
os.system("rm /var/cache/bind/db.%s" % (dominio))

#Fue todo correctamente
print "El usuario y su dominio fue borrado con exito."