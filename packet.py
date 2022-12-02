import struct
import time
from config import SEVENTY_YEARS_IN_SECONDS, BITE_OFFSET


class SNTP:
    HEADER_FORMAT = '> B B B B I I 4s Q Q Q Q'
    LEAP_INDICATOR = 0
    VERSION_NUMBER = 3
    MODE = 4
    STRATUM = 2
    FIRST_OCTET = LEAP_INDICATOR << 6 | VERSION_NUMBER << 3 | MODE
    CLIENT_REQUEST = '\x1b' + 47 * '\0'

    def __init__(self, time_delta=0):
        self.received_time = self.get_transmit_time()
        self.originate_time = 0
        self.time_delta = time_delta

    def analise_packet(self, received_packet):
        print("Analise packet: ")
        self.originate_time = struct.unpack(self.HEADER_FORMAT, received_packet)[10]
        print(self.originate_time)

    def get_server_packet(self, hora_server):
        return struct.pack(self.HEADER_FORMAT, self.FIRST_OCTET,
                           self.STRATUM, 0, 0, 0, 0, b'', 0,
                           self.originate_time, self.received_time,
                           self.get_transmit_time(self.time_delta, hora_server))

    def get_transmit_time(self, time_delta=0, hora_server=time.time()):
        now = hora_server
        actual_time = now + time_delta
        return int(actual_time * BITE_OFFSET)