
import logging
from queue import Queue

from communication_utils.comm_manager import CommManager

logger = logging.getLogger(__name__)

class App_IOBase():
    def __init__(self, comm_manager):
        self._comm_manager = CommManager(comm_manager)
        self._comm_manager.start_receive_and_process_threads()
        self._command_queues = {}
        self._timeout = 1.0
        self.timeout_callback = None
    
    def set_timeout_callback(self, call_back):
        self.timeout_callback = call_back
    
    def _get_queue(self, comm_id):

        queue = self._command_queues.get(comm_id, None)
        if not queue:
            self._command_queues[comm_id] = Queue()
        return self._command_queues[comm_id]

    def _get_queue_data(self, queue):
        response_data = ""
        try:
            response_data = queue.get(timeout=self._timeout)
        except Exception as e:
            logger.debug("No data received, reason {}".format(e))
        return response_data

    def default_callback(self, data, comm_id):
        if data != None:
            print(data)
            self._get_queue(comm_id).put(data)

    def set_timeout(self, timeout_value: float):
        self._timeout = timeout_value
