
import sys
import logging
from logging import handlers
pc_app_logger = logging.getLogger(__name__)

from communication_utils.udp_socket_interface import UDPSocket_CommInterface
from command_utils.instant_resp_commands import App_InstantRespCommandApp

def time_out_callback(comnd):
    print("RX response timeout for the command: {}".format(comnd))

class CLI:

    def __init__(self, target_ip, target_port) -> None:
        self.comm_interface = UDPSocket_CommInterface(target_ip, target_port)
        self.instant_cmnd = App_InstantRespCommandApp(self.comm_interface)
        self.instant_cmnd.set_timeout_callback(time_out_callback)


if __name__ == "__main__":

    cli = CLI('127.0.0.1', 20001)
    print(cli.instant_cmnd.send_command_recv_resp(("Hello world").encode()))
