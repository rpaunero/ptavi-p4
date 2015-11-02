#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import socketserver
import sys
import json
import time


class SIPRegisterHandler(socketserver.DatagramRequestHandler):
    """
    Echo server class
    """
    
    dicc = {}

    def register2json(self):
        with open('registered.json', 'w') as ff:
            json.dump(self.dicc, ff)

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
            
            line = line.decode('utf-8')
            print("El cliente nos manda " + line)
           
                     
            elemento = line.split(' ')            
            if elemento[0] == 'REGISTER':
                if not '@' in elemento[1].split(':')[1]:
                   break
                else:
                    direccion = elemento[1].split(':')[1]
                    time_expires = time.gmtime(time.time() + int(elemento[-2]))
                    time_expires = time.strftime('%Y-%m-%d %H:%M:%S', time_expires)
                    current_time = time.gmtime(time.time())
                    current_time = time.strftime('%Y-%m-%d %H:%M:%S', current_time)
                    self.dicc[direccion] = [IP, time_expires]
                    print('IP traza:' + IP)
                    print('Expires traza:' + time_expires)
                    print(time_expires + ('....') + current_time)
                    if (time_expires <= current_time):
                        del self.dicc[direccion]
                        print('eliminamos:' + direccion)
            self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")
            self.register2json()
            # Si no hay más líneas salimos del bucle infinito
            if not line:
                break

if __name__ == "__main__":
    # Creamos servidor de eco y escuchamos 
    serv = socketserver.UDPServer(('',int(sys.argv[1])), SIPRegisterHandler)
    print("Lanzando servidor UDP de eco...")
    serv.serve_forever()
