import logging
import threading
from queue import Queue
from utils import app_utils

comm_agent_logger = logging.getLogger(__name__)


class CommandRequest(object):
    def __init__(self, command, callback) -> None:
        self.command = command
        self.callback = callback

    def get_command(self):
        return self.command

    def get_callback(self):
        return self.callback


class CommAgent(object):
    def __init__(self, comm_interface) -> None:
        self.comm_interface = comm_interface
        self.commands_queue = Queue()
        self.kill_command_processing_thread = threading.Event()

    def issue_command(self, command, callback):
        cmd_request = CommandRequest(command, callback)
        self.commands_queue.put(cmd_request)

    def start_command_processing(self):
        command_processing_thread = threading.Thread(target=self.process_commands)
        command_processing_thread.setDaemon(True)
        command_processing_thread.name = f"command_processing_thread"
        command_processing_thread.start()

    def stop_command_processing(self):
        self.kill_command_processing_thread.set()

    def process_commands(self):
        while True:
            if self.kill_command_processing_thread.isSet():
                break

            cmd_request = self.commands_queue.get()
            request_encoder = app_utils.RequestEncoder()
            encoded_request = request_encoder.encode_command(cmd_request.get_command())

            if encoded_request is not None:
                self.comm_interface.send(encoded_request)

                response_decoder = app_utils.ResponseDecoder()

                #Start receiving the response.
                while response_decoder.is_packet_complete() == False:
                    raw_response = self.comm_interface.recv()
                    if len(raw_response) > 0:
                        response_decoder.decode_response(raw_response)
                    else:
                        comm_agent_logger.error(f"Failed to receive response!")
                        break

                decoded_response = response_decoder.get_decoded_response()
                callback = cmd_request.get_callback()
                callback(decoded_response)
            else:
                comm_agent_logger.error(f"Failed to encode request: {cmd_request}")
