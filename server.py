#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import socketserver
import sys

class SIPRegisterHandler(socketserver.DatagramRequestHandler):
    """
    Echo server class
    """
    
    dicc = {}

    def handle(self):
        #print(self.client_address)
        IP = self.client_address[0]
        print('IP' + ':' + IP)
        PORT = self.client_address[1]
        print('PORT' + ':' + str(PORT))
        
        # Escribe dirección y puerto del cliente (de tupla client_address)
        
        while 1:
            # Leyendo línea a línea lo que nos envía el cliente
            line = self.rfile.read()
            
            print("El cliente nos manda " + line.decode('utf-8'))
            line = line.decode('utf-8')
                     
            elemento = line.split(' ')            
            if elemento[0] == 'REGISTER':
                if not '@' in elemento[1].split(':')[1]:
                   break
                else: 
                    direccion = elemento[1].split(':')[1]
                    self.dicc[direccion] = IP
                    if elemento[-2] == 0:
                        dicc.pop(direccion)
            self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")
            # Si no hay más líneas salimos del bucle infinito
            if not line:
                break

if __name__ == "__main__":
    # Creamos servidor de eco y escuchamos 
    serv = socketserver.UDPServer(('',int(sys.argv[1])), SIPRegisterHandler)
    print("Lanzando servidor UDP de eco...")
    serv.serve_forever()
