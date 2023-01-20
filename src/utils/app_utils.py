import secrets
import logging
from collections import defaultdict

util_lib_logger = logging.getLogger(__name__)

PACKET_HEADER_SIZE      = 8
PACKET_START_MARKER     = 0x55


class ResponseDecoder(object):
    def __init__(self, request_id) -> None:
        self.request_id = request_id
        self.header_received = False
        self.unconsumed_response = bytearray()
        self.remaining_chunk_length = None
        self.cur_chunk_number = None
        self.packet_complete = False
        self.valid_packet = True
        self.chunks = defaultdict(bytearray)

    def decode_response(self, raw_response):
        self.unconsumed_response += raw_response

        while len(self.unconsumed_response) > 0 and ( self.packet_complete == False ) and ( self.valid_packet == True ):
            if not self.header_received:
                if len(self.unconsumed_response) >= PACKET_HEADER_SIZE:
                    self.decode_header()
                else:
                    # Not enough bytes yet for a header.
                    break
            else:
                self.decode_body()

    def is_packet_complete(self):
        return self.packet_complete

    def is_packet_valid(self):
        return self.valid_packet

    def get_decoded_response(self):
        if not self.valid_packet:
            util_lib_logger.critical(f"Invalid response!")
            return None

        chunk_numbers = self.chunks.keys()
        chunk_numbers = sorted(chunk_numbers)
        missing_chunks = [n for n in range(1,len(chunk_numbers)+1) if n not in chunk_numbers]
        if len(missing_chunks) > 0:
            util_lib_logger.critical(f"Missing chunks!")
            return None

        resp = bytearray()
        for chunk in chunk_numbers:
            resp += self.chunks[chunk]

        # If the actual packet got lost and we only got
        # end marker.
        if len(resp) == 0:
            resp = None

        return resp


    def decode_header(self):
        start_marker = self.unconsumed_response[0]
        chunk_number = self.unconsumed_response[1]
        chunk_length = (self.unconsumed_response[2] << 8) | (self.unconsumed_response[3] & 0xFF)
        request_id = self.unconsumed_response[4:8]

        if start_marker != PACKET_START_MARKER:
            self.valid_packet = False
            self.packet_complete = True
            return

        if request_id != self.request_id:
            self.valid_packet = False
            self.packet_complete = True
            return

        if chunk_length == 0:
            # last chunk received
            self.packet_complete = True
            return

        self.unconsumed_response = self.unconsumed_response[8:]
        self.remaining_chunk_length = chunk_length
        self.cur_chunk_number = chunk_number

        self.header_received = True

    def decode_body(self):
        if len(self.unconsumed_response) >= self.remaining_chunk_length:
            self.chunks[self.cur_chunk_number] += self.unconsumed_response[:self.remaining_chunk_length]
            self.unconsumed_response = self.unconsumed_response[self.remaining_chunk_length:]
            # We now expect header for next chunk
            self.header_received = False
        else:
            self.chunks[self.cur_chunk_number] += self.unconsumed_response
            self.remaining_chunk_length -= len(self.unconsumed_response)
            self.unconsumed_response = bytearray()


class RequestEncoder(object):
    def __init__(self) -> None:
        pass

    def encode_command(self, command):
        try:
            command = command.encode('ascii')
        except Exception as e:
            util_lib_logger.critical(f"Cant encode command: {e}")
            return None, None

        command_len = len(command)
        total_len = command_len + PACKET_HEADER_SIZE

        encoded_command = bytearray(total_len)
        encoded_command[0] = PACKET_START_MARKER
        encoded_command[1] = 1 # packet number
        # Next two bytes are length of actual command encoded in
        # network byte order.
        encoded_command[2] = command_len >> 8
        encoded_command[3] = command_len & 0xFF

        # Next 4 bytes are request id.
        request_id = secrets.token_bytes(4)
        encoded_command[4:] = request_id

        # Actual command comes after that.
        encoded_command[8:] = bytearray(command)

        return encoded_command, request_id
