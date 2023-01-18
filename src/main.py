
import sys
import time
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

    # """ Init CLI """
    # cli = CLI('127.0.0.1', 20001)

    # for i in range(10):
    #     """ Send commands """
    #     print(cli.instant_cmnd.send_command_recv_resp("ABCD"))
    #     time.sleep(1)
    
    # """ Exit """
    # cli.cli_close()

    bytes_data = app_utils.encode_packet("ABCD", 0)
    print(bytes_data)

    cmnd_type, to_str = app_utils.decode_packet(bytes_data)
    print(cmnd_type, to_str)
    