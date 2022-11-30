import socket
import time
import random
#import utilities2

localIP     = "127.0.0.1"
localPort   = 20001
bufferSize  = 32*9
msgFromServer       = "Mensaje recibido"
bytesToSend         = str.encode(msgFromServer)

# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind to address and ip
UDPServerSocket.bind((localIP, localPort))
print("Link Available")
bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)

while(True):

    print("Mensaje: {}\n\tIP local: {}\n\tPuerto: {}".format(bytesAddressPair[0].decode(),bytesAddressPair[1][0],bytesAddressPair[1][1]))

    UDPServerSocket.sendto("0".encode(), bytesAddressPair[1])
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    print("dentro: ",bytesAddressPair[0].decode())

while(True):
    if (bytesAddressPair[1][1] == direccion):

        tiempo_retardo = retardo()
        if (bytesAddressPair[0] == "fin".encode()): #El cliente termina de enviar el nombre, inicializar variables
            print("Nombre recibido por cliente = {}".format(mensaje_entero))
            mensaje_entero=""#String vacio para el nuevo nombre
            direcciones.pop(direccion)#Eliminar del diccionario la direccion usada
            try:
                direccion = next(iter(direcciones))#Si el largo del diccionario = 0, error y da paso a esperar otros clientes
                UDPServerSocket.sendto("0".encode(),(bytesAddressPair[1][0],direccion))   
            except:
                print("ESPERANDO DIRECCIONES")

        elif errorPerdida(): # 30% de probabilidad de perdida: entra si no hubo perdida
            message = bytesAddressPair[0].decode()
            address = bytesAddressPair[1]
            
            #CRC del mensaje recibido
            ans = utilities2.decodeData(message.encode(), key)

            if not errorPerdida(2):# 30% de probabilidad de error en CRC
                ans = errorCRC(ans) # Simulamos el error de CRC

            temp = "0" * (len(key) - 1)
            
            if ans != temp:
                msgFromServer = "Mensaje perdido por CRC"
                UDPServerSocket.sendto(msgFromServer.encode(),bytesAddressPair[1])#Envia al cliente el mensaje de la perdida por CRC
                print(msgFromServer)
            else: 
                msgFromServer = "Mensaje recibido"

                if tiempo_retardo<2:
                    car =chr(int((message[:len(message)-len(key)+1]),2))
                    mensaje_entero += car
                    UDPServerSocket.sendto(msgFromServer.encode(),bytesAddressPair[1])    

                else: 
                    UDPServerSocket.sendto("Mensaje perdido por retardo".encode(),bytesAddressPair[1])
                    print("ERROR. Tiempo de retardo: ", tiempo_retardo)
        else: # error de perdida
            UDPServerSocket.sendto("Mensaje perdido".encode(),bytesAddressPair[1])
            print("ERROR de perdida") 
    else: #Entra si la direccion del mensaje recibido es distinta al cliente actual

        id = bytesAddressPair[1][1]
        if id in direcciones: #Si ya esta guardada la direccion, guarda el caracter que dejó
            direcciones[id] = direcciones[id][1]+bytesAddressPair[0]
        else:# Si no esta en el diccionario, lo guarda
            direcciones[id] = bytesAddressPair[0]
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)

    if (len(direcciones) == 0):# Si esta vacio, cambia la variable direccion por la del mensaje del cliente y lo guarda en el diccionario
        direccion = bytesAddressPair[1][1]
        direcciones[direccion] = bytesAddressPair[0]