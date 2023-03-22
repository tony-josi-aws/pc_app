import socket

import logging
tcp_sock_logger = logging.getLogger(__name__)

class TCPSocket_CommInterface:

    def __init__(self, target_ip, target_port) -> None:

        self.target_ip = target_ip
        self.target_port = int(target_port)
        self.tcp_socket = None
        self.connect()
        self.set_timeout(0.5)

    def connect(self):
        try:
            self.tcp_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
            self.tcp_socket.connect((self.target_ip, self.target_port))
        except Exception as e:
            tcp_sock_logger.critical(f"TCP connect failed : {e}.", exc_info=True)

    def recv(self, bytes_to_receive = 2048):
        try:
            while True:
                rx_data = self.tcp_socket.recv(bytes_to_receive)
                if rx_data != None:
                    break
            return rx_data
        except Exception as e:
            tcp_sock_logger.critical(f"TCP get_rx failed : {e}.", exc_info=True)

    def send(self, data_bytes):
        try:
            self.tcp_socket.sendall(data_bytes)
        except Exception as e:
            tcp_sock_logger.critical(f"TCP send failed : {e}.", exc_info=True)

    def set_timeout(self, timeout):
        self.tcp_socket.settimeout(timeout)

    def close_interface(self):
        self.tcp_socket.close()
