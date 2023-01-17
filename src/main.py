
import sys
import logging
from logging import handlers
pc_app_logger = logging.getLogger(__name__)

from utils import app_utils
from communication_utils.udp_socket_interface import UDPSocket_CommInterface
from command_utils.instant_resp_commands import App_InstantRespCommandApp

def time_out_callback(comnd):
    pass

class CLI:

    def __init__(self, target_ip, target_port) -> None:
        self.comm_interface = UDPSocket_CommInterface(target_ip, target_port)
        self.instant_cmnd = App_InstantRespCommandApp(self.comm_interface)
        self.instant_cmnd.set_timeout_callback(time_out_callback)

    def cli_close(self):
        self.instant_cmnd._comm_manager.close()
        self.comm_interface.close_interface()

if __name__ == "__main__":

    for i in data:
        print(i)

    """ Init CLI """
    cli = CLI('127.0.0.1', 20001)

    """ Send commands """
    print(cli.instant_cmnd.send_command_recv_resp(app_utils.encode_packet("ABCD", app_utils.COMMAND_TYPE_REQUEST)))
    
    """ Exit """
    cli.cli_close()

    