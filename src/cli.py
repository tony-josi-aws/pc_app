import random
import threading
from cmd import Cmd
from communication_utils.comm_agent import CommAgent
from communication_utils.udp_socket_interface import UDPSocket_CommInterface


class UI_Cli(Cmd):
    intro = "Welcome to the FreeRTOS Inspector shell! Type ? to list commands."
    prompt = '(FreeRTOS Inspector) '

    def __init__(self) -> None:
        super(UI_Cli, self).__init__()
        self.comm_interface = None
        self.comm_agent = None
        self.response_received = threading.Event()

    def do_connect(self, addr):
        'Connect to the device. Syntax: connect <ip> <port>'
        address = addr.split()
        if (len(address) < 2):
            print("Error: Incorrect address, should be: connect <ip> <port>")
            return
        target_ip = address[0]
        target_port = int(address[1])
        if self.comm_interface == None:
            self.comm_interface = UDPSocket_CommInterface(target_ip, target_port)
            self.comm_agent = CommAgent(self.comm_interface)
            self.comm_agent.start_command_processing()
        else:
            self.do_disconnect("")
            self.do_connect(target_ip, target_port)

    def numbers_to_strings(self, argument):
        switcher = {
            0: " Rx Packets      : ",
            1: " Tx Packets      : ",
            2: " Rx Packet Drop  : ",
            3: " Tx Packet Drop  : ",
            4: " Rx Bytes Send   : ",
            5: " Tx Bytes Recv   : "
        }
        return switcher.get(argument, "nothing")

    def print_header(self, count):
        if count == 0:
            var = "UDP "
        if count == 6:
            var = "TCP "
        if count == 12:
            var = "ICMP "
        if count == 18:
            var = "Performance "
        if count % 6 == 0 :
            print("---------------------------------")
            print("   " + f"{var}"+"Network Statistic")
            print("----------------------------------")

    def do_disconnect(self, cmnd):
        'Disconnect from the device. Syntax: disconnect'
        if self.comm_agent != None:
            self.comm_agent.stop_command_processing()
            self.comm_interface.close_interface()
            self.comm_interface = None
            self.comm_agent = None

    def do_exit(self, inp):
        'Exit this CLI. Syntax: exit'
        print("Exciting CLI...")
        self.do_disconnect("")
        return True

    def do_send(self, cmnd):
        'Send a command to the device. Syntax: send <command>'
        self.response_received.clear()
        self.comm_agent.issue_command(cmnd, self.select_callback_for_command(cmnd))
        # Wait for the response.
        self.response_received.wait()

    def select_callback_for_command(self, cmnd):
        callback = self.default_command_complete_callback
        if cmnd.strip() == "pcap get":
            callback =self.pcap_get_command_complete_callback
        if cmnd.strip().lower() == "netstat get":
            callback =self.netstat_get_command_complete_callback
        return callback

    def default_command_complete_callback(self, response):
        if response is not None:
            try:
                str_resp = response.decode(encoding = 'ascii')
                print(f"{str_resp}")
            except:
                print(response)
        else:
            print("Timed out while waiting for response!")
        # Signal the do_send function to return.
        self.response_received.set()

    def pcap_get_command_complete_callback(self, response):
        if response is not None:
            pcap_file_name = str(hex(random.getrandbits(64)))
            pcap_file_name = pcap_file_name[2:]
            pcap_file_name += ".pcap"

            with open(pcap_file_name, 'wb') as f:
                f.write(response)

            print(f"Generated PCAP dump file: {pcap_file_name}")
        else:
            print("Timed out while waiting for response!")
        # Signal the do_send function to return.
        self.response_received.set()

    def netstat_get_command_complete_callback(self, response):
        if response is not None:
            str_resp = response.decode(encoding = 'ascii')
            stat = str_resp.split(',')
            count = 0
            for i in stat:
                self.print_header(count)
                if count == 18:
                    break;
                print( self.numbers_to_strings(count%6) + i)
                count+=1

            perf = stat[-2:]
            print ("Rx Latency     : " + str(perf[0]))
            print ("Tx Latency     : " + str(perf[1]))
        else:
            print("Timed out while waiting for response!")
        # Signal the do_send function to return.
        self.response_received.set()

    def default(self, line):
        print("Unknown command... Type ? to list commands")


if __name__ == "__main__":
    UI_Cli().cmdloop()
