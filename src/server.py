
import socket

from utils import app_utils

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

    cmnd_type, cmnd_data = app_utils.decode_packet(bytearray(message))

    clientMsg = app_utils.encode_packet(cmnd_data, 1)
    clientIP  = "Client IP Address:{}".format(address)
    
    print(clientMsg)
    print(clientIP)

    # # Sending a reply to client
    # bytesToSend = str.encode(clientMsg)

    UDPServerSocket.sendto(clientMsg, address)