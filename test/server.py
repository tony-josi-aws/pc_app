
import socket

INSTANT_RESP_CMND_ID    = 0xDE
PACKET_HEADER_SIZE      = 5

COMMAND_TYPE_REQUEST    = 0x00
COMMAND_TYPE_RESPONSE   = 0x01

def get_command_id(commnd_data):

    if len(commnd_data) > 2:
        return commnd_data[2]
    else:
        return 0xFF

def encode_packet(command_data, cmnd_type):

    try:
        command_data = command_data.encode('ascii')
    except Exception as e:
        return None

    command_len = len(command_data)
    total_len = command_len + PACKET_HEADER_SIZE
    data_bytes = bytearray(total_len)
    
    data_bytes[0] = 0x55
    data_bytes[total_len - 1] = 0xAA

    data_bytes[1] = 0 if cmnd_type == COMMAND_TYPE_REQUEST else 1

    data_bytes[2] = command_len >> 8
    data_bytes[3] = command_len & 0xFF

    data_bytes[4:total_len - 1] = bytearray(command_data)

    return data_bytes

def decode_packet(command_bytes):

    #for i in command_bytes:
        #print(i)

    command_type = COMMAND_TYPE_REQUEST if command_bytes[1] == COMMAND_TYPE_REQUEST else COMMAND_TYPE_RESPONSE

    data_len = command_bytes[2] 
    #print(command_bytes[3])
    data_len = (data_len << 8) | command_bytes[3]
    resp_data = bytearray(data_len)

    if (len(command_bytes) >= data_len + PACKET_HEADER_SIZE):
        resp_data = command_bytes[PACKET_HEADER_SIZE - 1 : + PACKET_HEADER_SIZE + data_len - 1].decode(encoding = 'ascii')

    return command_type, resp_data


localIP     = "127.0.0.1"

localPort   = 20001

bufferSize  = 1024

 

msgFromServer       = "Hello world! from SERVER!!"

bytesToSend         = str.encode(msgFromServer)

 

# Create a datagram socket

UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

 

# Bind to address and ip

UDPServerSocket.bind((localIP, localPort))

 

print("UDP server up and listening")

 

# Listen for incoming datagrams

while(True):

    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)

    message = bytesAddressPair[0]

    address = bytesAddressPair[1]

    cmnd_type, cmnd_data = decode_packet(bytearray(message))

    clientMsg = encode_packet(cmnd_data, 1)
    clientIP  = "Client IP Address:{}".format(address)
    
    print(clientMsg)
    print(clientIP)

    # # Sending a reply to client
    # bytesToSend = str.encode(clientMsg)

    UDPServerSocket.sendto(clientMsg, address)