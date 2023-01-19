

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

    prompt = '>>> '
    intro = "Welcome! Type ? to list commands"

    def __init__(self) -> None:
        super(UI_Cli, self).__init__()
        self.comm_interface = None
        self.instant_cmnd = None

    def do_connect(self, addr):
        address = addr.split()
        if (len(address) < 2):
            print("Error: Incorrect address, should be: connect <ip> <port>")
            return
        target_ip = address[0]
        target_port = int(address[1])
        if self.comm_interface == None:
            self.comm_interface = UDPSocket_CommInterface(target_ip, target_port)
            self.instant_cmnd = App_InstantRespCommandApp(self.comm_interface)
            self.instant_cmnd.set_timeout_callback(time_out_callback)
        else:
            self.do_close_connection("")
            self.do_connect(target_ip, target_port)

    def do_close_connection(self, cmnd):
        if self.instant_cmnd != None:
            self.instant_cmnd._comm_manager.close()
            self.comm_interface.close_interface()
            self.comm_interface = None
            self.instant_cmnd = None

    def do_exit(self, inp):
            print("Exciting CLI...")
            self.do_close_connection("")
            return True

    def do_send(self, cmnd):
        if cmnd.lower() == "pcap get":
            rx_data = self.instant_cmnd.send_command_recv_resp(cmnd, write_to_file = True)
        else:
            rx_data = self.instant_cmnd.send_command_recv_resp(cmnd)

        try:
            str_resp = rx_data[1].decode(encoding = 'ascii')
            print("RX Status: {}, Msg: {}".format("OK" if rx_data[0] == True else "FAIL" , str_resp))
        except:
            print("RX Status: {}, Msg: {}".format("OK" if rx_data[0] == True else "FAIL", rx_data[1]))

    def default(self, line):
        print("Unknown command... Type ? to list commands")

if __name__ == "__main__":

    UI_Cli().cmdloop()

