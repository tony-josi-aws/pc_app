import logging
import threading
from queue import Queue
from utils import app_utils

comm_agent_logger = logging.getLogger(__name__)


class CommandRequest(object):
    def __init__(self, command, callback, callback_data=None) -> None:
        self.command = command
        self.callback = callback
        self.callback_data = callback_data

    def get_command(self):
        return self.command

    def invoke_callback(self, response):
        if self.callback_data is None:
            self.callback(response)
        else:
            self.callback(response, self.callback_data)


class CommAgent(object):
    def __init__(self, comm_interface) -> None:
        self.comm_interface = comm_interface
        self.commands_queue = Queue()
        self.kill_command_processing_thread = threading.Event()

    def issue_command(self, command, callback, callback_data=None):
        cmd_request = CommandRequest(command, callback, callback_data)
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
            encoded_request, request_id = request_encoder.encode_command(cmd_request.get_command())

            if encoded_request is not None:
                self.comm_interface.send(encoded_request)

                decoded_response = None

                # Make 3 attempts to get a valid response.
                for i in range(3):
                    response_decoder = app_utils.ResponseDecoder(request_id)

                    # Start receiving the response.
                    while response_decoder.is_packet_complete() == False:
                        raw_response = self.comm_interface.recv()
                        if raw_response is not None and len(raw_response) > 0:
                            response_decoder.decode_response(raw_response)
                        else:
                            comm_agent_logger.error(f"Failed to receive response!")
                            break

                    if response_decoder.is_packet_complete() == True and response_decoder.is_packet_valid() == True:
                        decoded_response = response_decoder.get_decoded_response()
                        break

                cmd_request.invoke_callback(decoded_response)
            else:
                comm_agent_logger.error(f"Failed to encode request: {cmd_request}")
