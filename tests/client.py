import socket
import struct

# initize sockets and connection
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '192.168.4.1'
serverPort = 7777

# connect to host
s.connect((host, serverPort))
 
send = "";
while send != "stop":
    send = input(": ")
    packet = send
    print("sending", packet) 
    s.send(packet.encode())
    

s.close()
