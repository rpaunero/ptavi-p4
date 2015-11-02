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
        try:
            with open('registered.json', 'w') as ff:
                json.dump(self.dicc, ff)
        except:
            pass

    def json2register(self):
        try:
            with open('registered.json', 'r') as ff:
                self.dicc = json.load(ff)
        except:
            pass


    def handle(self):
        #print(self.client_address)
        IP = self.client_address[0]
        print('IP' + ':' + IP)
        PORT = self.client_address[1]
        print('PORT' + ':' + str(PORT))
        
        # Escribe dirección y puerto del cliente (de tupla client_address)
        self.json2register()
        
        while 1:
            # Leyendo línea a línea lo que nos envía el cliente
            line = self.rfile.read()
            if not line:
                break
            
            line = line.decode('utf-8')
            print("El cliente nos manda " + line)
           
                     
            elemento = line.split(' ')            
            if elemento[0] == 'REGISTER':
                if not '@' in elemento[1].split(':')[1]:
                   break

                formato = '%Y-%m-%d %H:%M:%S'
                direccion = elemento[1].split(':')[1]
                time_expires1 = time.gmtime(time.time() + int(elemento[-2]))
                time_expires = time.strftime(formato, time_expires1)
                current_time1 = time.gmtime(time.time())
                current_time = time.strftime(formato, current_time1)
                self.dicc[direccion] = [IP, time_expires]
                print('IP traza:' + IP)
                print('Expires traza:' + time_expires)
                print(time_expires + ('....') + current_time)


                temp_list = []
                for usuario in self.dicc:
                   
                   if (time.strptime(self.dicc[usuario][1], formato) <= current_time1):
                       temp_list.append(usuario) 
                       print('Añado a : ' + usuario + 'lista temporal')
                            #del self.dicc[direccion]
                            #print('eliminamos:' + direccion)
                for usuario in temp_list:
                    del self.dicc[usuario]
                    print('eliminamos:' + usuario)
                self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")
                self.register2json()

            # Si no hay más líneas salimos del bucle infinito

if __name__ == "__main__":
    # Creamos servidor de eco y escuchamos 
    serv = socketserver.UDPServer(('',int(sys.argv[1])), SIPRegisterHandler)
    print("Lanzando servidor UDP de eco...")
    serv.serve_forever()
