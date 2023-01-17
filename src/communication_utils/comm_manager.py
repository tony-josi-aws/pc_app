

import os
import binascii
import threading
import time
from queue import Queue

import logging
comm_manager_logger = logging.getLogger(__name__)

from utils import app_utils

class CommManager:

    def __init__(self, interface_handle) -> None:
        """
        Init
        """
        self.rx_queue = Queue()
        self.callback_list = {}
        self.lock = threading.Lock()
        self.command_logging = None
        self.interface_handle = interface_handle
        self._kill_threads = threading.Event()
        self.receive_thread = threading.Thread(target=self.read_interface_rx)


    def read_interface_rx(self):
        """
        Reads packet from interface port and store it in queue.
        """

        """ Small delay to wait till the socket get created """
        time.sleep(0.1) 
        while True:
            try:
                if self._kill_threads.isSet():
                    break
                """ Blocking call """
                data_bytes = self.interface_handle.get_rx()
                self.rx_queue.put(data_bytes)
            except Exception as e:
                comm_manager_logger.critical(f"read_interface_rx thread failed : {e}.", exc_info=True)
                break    

    def process_queue(self):
        """
        Reads the packet from queue and send to relevant callback function.
        """
        while True:
            try:
                

                rx_data = self.rx_queue.get()
                #print("++++++++++++ {}".format(rx_data))
                rx_data_id =  app_utils.get_command_id(rx_data)
                rx_data = rx_data.decode()

                if self._kill_threads.isSet():
                    break

                """ Do callbacks """
                callback = self.callback_list.get(rx_data_id, [])
                if callback:
                    #print("=================== callback found")
                    callback(rx_data, rx_data_id)
                else:
                    comm_manager_logger.warning(f"Received an unexpected packet {rx_data} with packet ID {rx_data_id}")
            except Exception as e:
                comm_manager_logger.critical(f"Process_queue thread failed : {e}.", exc_info=True)
                # TODO: break or move on? 
                
    def write_interface_tx(self, tx_data_bytes):
        try:
            self.interface_handle.send_data_bytes(tx_data_bytes)
        except Exception as e:
            comm_manager_logger.critical("Failed to do a interface write: " + tx_data_bytes + " Excep: " + str(e))    

    def start_receive_and_process_threads(self):
        """
        start process and receive thread.
        """
        self.receive_thread.setDaemon(True)
        self.receive_thread.start()
        thread = threading.Thread(target=self.process_queue)
        thread.setDaemon(True)
        thread.name = f"process_thread"
        thread.start()


    def subscribe(self, rx_data_id, callback):
        """
        Subscribe packet id to the callback.
        """
        self.callback_list[rx_data_id] = callback

    def unsubscribe(self, rx_data_id, application_callback):
        """
        Unsubscribe packet id and removes the callback.
        """
        self.callback_list[rx_data_id] = None

    def close(self):
        """
        Closes interface port
        """
        self._kill_threads.set()
        # # to free up queue.get() lock in process_queue add -1 to queue
        # self.rx_queue.put(-1)
