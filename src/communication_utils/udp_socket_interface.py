import socket

import logging
udp_sock_logger = logging.getLogger(__name__)

class UDPSocket_CommInterface:
    
    def __init__(self, target_ip, target_port) -> None:

        self.target_ip = target_ip
        self.target_port = target_port
        self.udp_socket = None
        self.connect()

    def connect(self):
        try:
            self.udp_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
            #self.udp_socket.bind((self.target_ip, self.target_port))
        except Exception as e:
            udp_sock_logger.critical(f"UDP connect failed : {e}.", exc_info=True)

    def get_rx(self, bytes_to_receive = 1024):
        try:
            rx_data = self.udp_socket.recvfrom(bytes_to_receive)
            #print(rx_data)
            return rx_data[0]
        except Exception as e:
            #udp_sock_logger.critical(f"UDP get_rx failed : {e}.", exc_info=True)
            pass


    def send_data_bytes(self, data_bytes):
        try:
            self.udp_socket.sendto(data_bytes, (self.target_ip, self.target_port))      
        except Exception as e:
            udp_sock_logger.critical(f"UDP send_data_bytes failed : {e}.", exc_info=True)

    def set_timeout(self, timeout):
        self.udp_socket.settimeout(timeout)

    def close_interface(self):
        self.udp_socket.close()
          