# ­*­ coding: utf­8 ­*­

import sys
import os
import MySQLdb

#Pedimos nombre de usuario, la contrasena a cambiar (mysql o ftp) y la nueva contrasena
usuario=sys.argv[1]
sistema=sys.argv[2]
contrasenanueva=sys.argv[3]

#Comprobamos que existe y si es asi cambiamos las passwords segun el sistema
if sistema == "mysql"
	if os.path.isdir("/var/www/%s" % (usuario)) == True:
		#Abrimos una conexion con la base de datos de mysql
		base = MySQLdb.connect(host="localhost", user="root", passwd="usuario", db="mysql")
		cursor=base.cursor()
		cambio="SET PASSWORD FOR my%s@localhost = PASSWORD('%s');" % (usuario,contrasenanueva)
		cursor.execute(cambio)
		base.commit()
		print "contrasenna actualizada correctamente"
	else:
		print "El usuario %s no existe, introduzca otro usuario por favor." % (usuario)
		exit()
else sistema == "ftp":
	if os.path.isdir("/var/www/%s" % (usuario)) == True:
		#Abrimos una conexion con la base de datos que contiene los usuarios virtuales
		base2 = MySQLdb.connect(host="localhost", user="root", passwd="usuario", db="ftp")
		cursor2=base2.cursor2()
		cambio2="update usuarios set password = PASSWORD('%s')where username='%s';" % (contrasenanueva,usuario)
		cursor2.execute(cambio2)
		base2.commit()
		print "contrasenna actualizada correctamente"
	else:
		print "El usuario %s no existe, introduzca otro usuario por favor." % (usuario)
		exit()