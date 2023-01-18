

import sys
import time
import logging
from cmd import Cmd
from logging import handlers
pc_app_logger = logging.getLogger(__name__)

from utils import app_utils
from communication_utils.udp_socket_interface import UDPSocket_CommInterface
from command_utils.instant_resp_commands import App_InstantRespCommandApp

def time_out_callback(comnd):
    pass


class UI_Cli(Cmd):

    def __init__(self) -> None:
        super(UI_Cli, self).__init__()
        self.comm_interface = None
        self.instant_cmnd = None

    def do_connect(self, address):
        target_ip = address.split()[0]
        target_port = int(address.split()[1])
        if self.comm_interface == None:
            self.comm_interface = UDPSocket_CommInterface(target_ip, target_port)
            self.instant_cmnd = App_InstantRespCommandApp(self.comm_interface)
            self.instant_cmnd.set_timeout_callback(time_out_callback)
        else:
            self.do_close_connection()
            self.do_connect(target_ip, target_port)

    def do_close_connection(self):
        self.instant_cmnd._comm_manager.close()
        self.comm_interface.close_interface()
        self.comm_interface = None
        self.instant_cmnd = None

    def do_exit(self, inp):
            print("Exciting CLI...")
            self.do_close_connection()
            return True

    def do_send(self, cmnd):
        rx_data = self.instant_cmnd.send_command_recv_resp(cmnd)
        # cmnd_type, cmnd_data = app_utils.decode_packet(rx_data)
        # print("RX Type: {}".format(cmnd_type))
        print("RX Msg: {}".format(rx_data))

if __name__ == "__main__":

    UI_Cli().cmdloop()

    