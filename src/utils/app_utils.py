import re
import logging

util_lib_logger = logging.getLogger(__name__)

INSTANT_RESP_CMND_ID = 0xDE

def get_command_id(commnd_data):

    if len(commnd_data) > 2:
        return commnd_data[2]
    else:
        return 0xFF

