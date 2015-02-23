# ­*­ coding: utf­8 ­*­

import sys
import os
import MySQLdb
import string
from random import choice

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
#Introducimos el index en construccion
ficheroindex = open("plantillas/index.html","r")
lineas2 = ficheroindex.read()
ficheroindex.close()
os.system("touch /var/www/%s/index.html" % (usuario))
index = open("/var/www/%s/index.html" % (usuario),"w")
lineas2 = lineas2.replace('**dominio**',dominio)
index.write(lineas2)
index.close()
#Activamos el sitio y reiniciamos Apache2
os.system("a2ensite %s>/dev/null" % (dominio))
os.system("service apache2 restart>/dev/null")

#Introducir las zonas nuevas a named.conf.local
linea3 = '\nzone ' +'"' + dominio +'"' +'{\ntype master;\nfile "db.'+ dominio +'"' +';\n}; '
ficheronamed = open("/etc/bind/named.conf.local","a")
ficheronamed.write(linea3)
ficheronamed.close()

#Ficheros de la zona nueva
plantillazonadb = open("plantillas/zonadb","r")
lineas3 = plantillazonadb.read()
plantillazonadb.close()
ficherozonadb = open("/var/cache/bind/db.%s" % (dominio),"w")
lineas3 = lineas3.replace('**dominio**',dominio)
ficherozonadb.write(lineas3)
ficherozonadb.close()

os.system("service bind9 restart>/dev/null")

#Generar contrasena aleatoria para mysql
def GenPasswd(n):
	return ''.join([choice(string.letters + string.digits) for i in range(n)])
contrasennamysql=GenPasswd(8)

#Creacion de la base de datos y usuario en MySQL
os.system("mysql -u root -pusuario -e 'create user '%s'@'localhost' identified by '%s';'" % (usuario,contrasennamysql))
os.system("mysql -u root -pusuario -e 'create database %s;'" % (usuario))
os.system("mysql -u root -pusuario -e 'grant all on %s.* to %s identified by '%s';'" % (usuario,usuario,contrasennamysql))

#Habilitar acceso ftp
#Generar contrasena aleatoria para ftp
def GenPasswd(n):
	return ''.join([choice(string.letters + string.digits) for i in range(n)])
contrasenna=GenPasswd(8)
#Abrimos una conexion con la base de datos que contiene los usuarios virtuales
base = MySQLdb.connect(host="localhost", user="root", passwd="usuario", db="ftp")
cursor=base.cursor()

#insertamos el usuario
consultauid="select max(uid) from usuarios;"
cursor.execute(consultauid)
consulta_uid = cursor.fetchone()
#si la tabla esta vacia introduce el 3001
if consulta_uid[0] == None:
	conuid=str("3001")
	usermysql="insert into usuarios values('"+ usuario+"'," +"PASSWORD('"+contrasenna+"'),"+conuid+","+conuid+","+"'/var/www/"+usuario+"',"+"'/bin/false1',"+"1,'"+dominio+"');"
	cursor.execute(usermysql)
	base.commit()
#cambiamos el propietario de la carpeta /var/www
	os.system("chown -R %s:%s /var/www/%s" % (conuid,conuid,usuario))
#en caso contrario le suma uno al numero maximo de la tabla
else:
	conuid=consulta_uid[0]+1
	conuidn=str(conuid)
	usermysql="insert into usuarios values('"+ usuario+"'," +"PASSWORD('"+contrasenna+"'),"+conuidn+","+conuidn+","+"'/var/www/"+usuario+"',"+"'/bin/false1',"+"1,'"+dominio+"');"
	cursor.execute(usermysql)
	base.commit()
#cambiamos el propietario de la carpeta /var/www
	os.system("chown -R %s:%s /var/www/%s" % (conuid,conuid,usuario))

#Fue todo bien
print "El usuario y su dominio se crearon con exito"
print"Esta es tu contrasena para MySql:%s"% (contrasennamysql)
print"Esta es tu contrasena para el ftp:%s"% (contrasenna)