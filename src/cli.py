import threading
from cmd import Cmd
from communication_utils.comm_agent import CommAgent
from communication_utils.udp_socket_interface import UDPSocket_CommInterface
from utils.network_stats_deserializer import deserialize_network_stats
from utils.kernel_stats_deserializer import deserialize_kernel_stats
from utils.core_dump_parser import core_dump_parser
from utils.log2tdi import convert_raw_logs_to_tdi

class UI_Cli(Cmd):
    intro = "Welcome to the FreeRTOS Inspector shell! Type ? to list commands."
    prompt = 'FreeRTOS Inspector$ '

    def __init__(self) -> None:
        super(UI_Cli, self).__init__()
        self.comm_interface = None
        self.comm_agent = None
        self.response_received = threading.Event()

    def do_help(self, cmd):
        if not cmd:
            print('\nThe following commands are available:\n')
            print('1. connect - Connect to a device.')
            print('2. disconnect - Disconnect from a device.')
            print('3. top - List tasks running on the device.')
            print('4. netstat - List network statistics from the device.')
            print('5. firewall - View, add or modify firewall rules for the device.')
            print('6. trace - Get execution trace from the device.')
            print('7. pcap - Get network traffic from the device.')
            print('8. coredump - Get coredump from the device.')
            print('9. exit - Exit from the CLI.')
            print('10. help - Get help.')
            print('\nType "help <command>" for a command specific help.\n')

        if cmd == 'connect':
            print('\nConnect to a device.')
            print('Syntax: connect <ip> <port>\n')

        if cmd == 'disconnect':
            print('\nDisconnect from a device.')
            print('Syntax: disconnect\n')

        if cmd == 'top':
            print('\nList tasks running on the device.')
            print('Syntax: top\n')

        if cmd == 'netstat':
            print('\nList network statistics from the device.')
            print('Syntax: netstat\n')

        if cmd == 'firewall':
            print('\nThe following sub-commands are available:\n')
            print('1. add - Add a firewall rule. Syntax: firewall add <src ip> <src port> <dst ip> <dst port> <protocol num> <permission>')
            print('   <protocol num> ICMP: 1, TCP: 6, UDP: 17')
            print('   <permission> Allow: 1, Block: 0')
            print('2. list - List all firewall rules. Syntax: firewall list')
            print('3. remove - Remove a firewall rule. Syntax: firewall remove\n')

        if cmd == 'trace':
            print('\nThe following sub-commands are available:\n')
            print('1. start - Start capturing execution traces on the device. Syntax: trace start')
            print('2. stop - Stop capturing execution traces on the device. Syntax: trace stop')
            print('3. get - Get execution traces fom the device. Syntax: trace get <output_file>\n')

        if cmd == 'pcap':
            print('\nThe following sub-commands are available:\n')
            print('1. start - Start capturing network traffic on the device. Syntax: pcap start')
            print('2. stop - Stop capturing network traffic on the device. Syntax: pcap stop')
            print('3. get - Get captured network traffic traces fom the device. Syntax: pcap get <output_file>\n')

        if cmd == 'coredump':
            print('\nThe following sub-commands are available:\n')
            print('1. check - Check if a coredump exists on the device. Syntax: coredump check')
            print('2. remove - Remove a coredump from the device. Syntax: coredump remove')
            print('3. get - Get coredump from the device. Syntax: coredump get <output_file>\n')

        if cmd == 'exit':
            print('\nExit from the CLI.')
            print('Syntax: exit\n')

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
        UI_Cli.prompt = f'FreeRTOS Inspector@{target_ip}:{target_port}$ '

    def do_disconnect(self, cmnd):
        'Disconnect from the device. Syntax: disconnect'
        if self.comm_agent != None:
            self.comm_agent.stop_command_processing()
            self.comm_interface.close_interface()
            self.comm_interface = None
            self.comm_agent = None
        UI_Cli.prompt = 'FreeRTOS Inspector$ '

    def do_exit(self, inp):
        'Exit this CLI. Syntax: exit'
        print("Exciting CLI...")
        self.do_disconnect("")
        return True

    def do_send(self, cmnd):
        'Send a command to the device. Syntax: send <command>'
        self.response_received.clear()
        if self.comm_agent != None:
            if "pcap get" in cmnd.strip().lower() or \
               "trace get" in cmnd.strip().lower() or \
               "coredump get" in cmnd.strip().lower():
                cmnd_words = cmnd.split()
                if len(cmnd_words) != 3:
                    print('Invalid command syntax!')
                else:
                    file_path = cmnd_words[2]
                    device_command = " ".join(cmnd_words[:2])

                    self.comm_agent.issue_command(device_command, self.select_callback_for_command(device_command), file_path)
                    # Wait for the response.
                    self.response_received.wait()
            else:
                self.comm_agent.issue_command(cmnd, self.select_callback_for_command(cmnd))
                # Wait for the response.
                self.response_received.wait()
        else:
            print('Connect to a device first!')

    def precmd(self, line):
        command_words = line.split()
        if len(command_words) > 0:
            if command_words[0] == 'firewall':
                if len(command_words) >= 2:
                    line = f'send {command_words[0]}-{command_words[1]} {" ".join(command_words[2:])}'
            elif command_words[0] not in ['connect', 'disconnect', 'exit', 'help', '?']:
                line = f'send {line}'
        return line

    def select_callback_for_command(self, cmnd):
        callback = self.default_command_complete_callback
        if cmnd.strip().lower() == "pcap get":
            callback =self.pcap_get_command_complete_callback
        if cmnd.strip().lower() == "trace get":
            callback =self.trace_get_command_complete_callback
        if cmnd.strip().lower() == "netstat":
            callback =self.netstat_command_complete_callback
        if cmnd.strip().lower() == "top":
            callback =self.top_command_complete_callback
        if cmnd.strip().lower() == "coredump get":
            callback =self.coredump_get_command_complete_callback
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

    def pcap_get_command_complete_callback(self, response, output_file):
        if response is not None:
            if not output_file.endswith('.pcap'):
                output_file += ".pcap"

            with open(output_file, 'wb') as f:
                f.write(response)

            print(f"Generated PCAP dump file: {output_file}")
        else:
            print("Timed out while waiting for response!")
        # Signal the do_send function to return.
        self.response_received.set()

    def coredump_get_command_complete_callback(self, response, output_file):
        if response is not None:
            if not output_file.endswith('.dump'):
                output_file += ".dump"

            temp_output_file = output_file + ".tmp"
            with open(temp_output_file, 'wb') as f:
                f.write(response)

            parser = core_dump_parser()
            parser.parse_core_dump(temp_output_file, output_file)

            print(f"Generated coredump file: {output_file}")
        else:
            print("Timed out while waiting for response!")
        # Signal the do_send function to return.
        self.response_received.set()

    def trace_get_command_complete_callback(self, response, output_file):
        if response is not None:
            if not output_file.endswith('.tdi'):
                output_file += ".tdi"

            temp_output_file = output_file + ".tmp"
            with open(temp_output_file, 'wb') as f:
                f.write(response)

            convert_raw_logs_to_tdi(temp_output_file, output_file)
            print(f"Generated Trace dump file: {output_file}")
        else:
            print("Timed out while waiting for response!")
        # Signal the do_send function to return.
        self.response_received.set()

    def netstat_command_complete_callback(self, response):
        if response is not None:
            str_resp = response.decode(encoding = 'ascii')
            deserialized_stats = deserialize_network_stats(str_resp)
            print(deserialized_stats)
        else:
            print("Timed out while waiting for response!")
        # Signal the do_send function to return.
        self.response_received.set()

    def top_command_complete_callback(self, response):
        if response is not None:
            str_resp = response.decode(encoding = 'ascii')
            deserialized_stats = deserialize_kernel_stats(str_resp)
            print(deserialized_stats)
        else:
            print("Timed out while waiting for response!")
        # Signal the do_send function to return.
        self.response_received.set()

    def default(self, line):
        print("Unknown command... Type ? to list commands")


if __name__ == "__main__":
    UI_Cli().cmdloop()
