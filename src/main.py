
import sys
import logging
from logging import handlers
pc_app_logger = logging.getLogger(__name__)

from communication_utils.udp_socket_interface import UDPSocket_CommInterface
from command_utils.instant_resp_commands import App_InstantRespCommandApp
class CLI:

    def __init__(self, target_ip, target_port) -> None:
        self.comm_interface = UDPSocket_CommInterface(target_ip, target_port)
        self.instant_cmnd = App_InstantRespCommandApp(self.comm_interface)


if __name__ == "__main__":

    cli = CLI('127.0.0.1', 20001)
    print(cli.instant_cmnd.send_command_recv_resp(("Hello world").encode()))
