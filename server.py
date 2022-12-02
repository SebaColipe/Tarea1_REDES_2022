import socket
from packet import SNTP
from config import PORT, IP, BUFFER_SIZE, NTP_SERVER, SEVENTY_YEARS_IN_SECONDS
import time
import struct

class Server:
    def __init__(self):
        self.delta = 0
        self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server.bind((IP, PORT))
        self.ntp_server = NTP_SERVER
        self.hora = 0
        print(f'Server start on {IP}:{PORT}')
    
    def check_time(self):
        client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        data = SNTP.CLIENT_REQUEST.encode('utf-8')
        client.sendto(data, (self.ntp_server, PORT))
        data, address = client.recvfrom(1024)
        self.hora = struct.unpack('!12I', data)[10]
        client.close()
        if data:
            print(f'Response from: {address[0]} : {address[1]}')
        print('\tTime: ' + str(time.ctime(struct.unpack('!12I', data)[10] - SEVENTY_YEARS_IN_SECONDS)))

    def run(self):
        while True:
            t1 = time.time()
            self.check_time()
            received_packet, address = self.server.recvfrom(BUFFER_SIZE)
            self.delta = time.time()-t1
            sntp = SNTP(self.delta)
            sntp.analise_packet(received_packet)
            packet = sntp.get_server_packet(hora_server = self.hora)
            self.server.sendto(packet, address)
            print(address, " acaba de preguntar")


if __name__ == '__main__':
    server = Server()
    server.run()