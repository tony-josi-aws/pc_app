import socket

import logging
udp_sock_logger = logging.getLogger(__name__)

class UDPSocket_CommInterface:

    def __init__(self, target_ip, target_port) -> None:

        self.target_ip = target_ip
        self.target_port = int(target_port)
        self.udp_socket = None
        self.connect()
        self.set_timeout(2)

    def connect(self):
        try:
            self.udp_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        except Exception as e:
            udp_sock_logger.critical(f"UDP connect failed : {e}.", exc_info=True)

    def recv(self, bytes_to_receive = 2048):
        try:
            rx_data = self.udp_socket.recvfrom(bytes_to_receive)
            return rx_data[0]
        except Exception as e:
            udp_sock_logger.info(f"UDP get_rx failed : {e}.", exc_info=True)

    def send(self, data_bytes):
        try:
            self.udp_socket.sendto(data_bytes, (self.target_ip, self.target_port))
        except Exception as e:
            udp_sock_logger.critical(f"UDP send failed : {e}.", exc_info=True)

    def set_timeout(self, timeout):
        self.udp_socket.settimeout(timeout)

    def close_interface(self):
        self.udp_socket.close()
