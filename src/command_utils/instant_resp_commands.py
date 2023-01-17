
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
        response_byte = ""
        response_byte = self._get_queue_data(queue)
        if response_byte == "":
            logger.error("RX response timeout for {}".format(command))
            self.timeout_callback(command)
        logger.debug(f"RX response :: {command} : {response_byte}")
        return response_byte
