
import time
import logging
from datetime import datetime

from .io_base import App_IOBase 
from utils import app_utils

logger = logging.getLogger(__name__)

class App_InstantRespCommandApp(App_IOBase):

    def __init__(self, comm_manager):
        super(App_InstantRespCommandApp, self).__init__(comm_manager)


    def send_command_recv_resp(self, command, command_type = app_utils.COMMAND_TYPE_REQUEST):

        command_id = app_utils.INSTANT_RESP_CMND_ID #app_utils.get_command_id(command)
        encoded_command = app_utils.encode_packet(command, command_type)

        logger.info(f"Sending command with ID: {command_id}, encoded data: {encoded_command}")
        queue = self._get_queue(command_id)
        self._comm_manager.subscribe(command_id, self.default_callback)
        self._comm_manager.write_interface_tx(encoded_command)

        response_info = ""

        while True:       

            header_data = ""
            header_data = self._get_queue_data(queue)
            if header_data == "":
                logger.error("RX response header timeout for {}".format(command))
                self.timeout_callback(command)

            header_info = app_utils.decode_header_packet(header_data)
            if (len(header_info) < 2):
                return None

            if header_info[1] == 0:
                break

            response_bytes = ""
            response_bytes = self._get_queue_data(queue)
            if response_bytes == "":
                logger.error("RX response data timeout for {}".format(command))
                self.timeout_callback(command)

            response_info_temp = app_utils.decode_data_packet(response_bytes)
            print(response_info_temp)
            response_info += response_info_temp


        logger.debug(f"RX response :: {command} : {response_info}")
        return response_info

