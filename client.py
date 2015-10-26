#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Programa cliente que abre un socket a un servidor
"""

import socket
import sys

    
# Cliente UDP simple.

# Dirección IP del servidor.
try:
    SERVER = sys.argv[1]
    PORT = int(sys.argv[2])
    REGISTER = sys.argv[3]
    DIRECCION = sys.argv[4]
    TIME = sys.argv[5]  
except IndexError:
    sys.exit('Usage: client.py ip puerto register sip_address expires_value')


# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
my_socket.connect((SERVER, PORT))

if sys.argv[3] == 'register':
    TIEMPO = ("Expires:" + ' ' + TIME + ' ' + '\r\n\r\n')
    REGISTER  = ('REGISTER' + ' ' + 'sip:' + sys.argv[4] + ' ' + 'SIP/2.0')
    my_socket.send(bytes(REGISTER , 'utf-8') + b'\r\n\r\n' + bytes(TIEMPO, 'utf-8'))
    data = my_socket.recv(1024)
    

print('Recibido -- ', data.decode('utf-8'))
print("Terminando socket...")

# Cerramos todo
my_socket.close()
print("Fin.")
