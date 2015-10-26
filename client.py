#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Programa cliente que abre un socket a un servidor
"""

import socket
import sys

    
# Cliente UDP simple.

# Dirección IP del servidor.
SERVER = sys.argv[1]
PORT = int(sys.argv[2])
# Contenido que vamos a enviar
#Line_List = sys.argv[3:]
#LINE = ' '.join(Line_List)

# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
my_socket.connect((SERVER, PORT))

if sys.argv[3] == 'register':
    REGISTER  = ('REGISTER' + ' ' + 'sip:' + sys.argv[4] + ' ' + 'SIP/2.0')
    #print("Enviando: " + LINE)
    my_socket.send(bytes(REGISTER, 'utf-8') + b'\r\n\r\n')
    data = my_socket.recv(1024)

print('Recibido -- ', data.decode('utf-8'))
print("Terminando socket...")

# Cerramos todo
my_socket.close()
print("Fin.")
