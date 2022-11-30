import socket
import sys

msgFromClient       = sys.argv[1]#"SEBASTIAN"

#bytesToSend         = str.encode(msgFromClient)
serverAddressPort   = ("127.0.0.1", 20001)
bufferSize          = 32*9

# Create a UDP socket at client side
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Send to server using created UDP socket
print("Intentando enviar")

UDPClientSocket.sendto(msgFromClient.encode(), serverAddressPort)
bytesAddressPair = UDPClientSocket.recvfrom(bufferSize)

print("Mensaje: {}\n\tIP local: {}\n\tPuerto: {}".format(bytesAddressPair[0].decode(),bytesAddressPair[1][0],bytesAddressPair[1][1]))

