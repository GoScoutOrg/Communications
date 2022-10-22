import socket
import struct

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# host = socket.gethostname()
host = '192.168.4.1'
port = 7777

print(host, port, s)
 
# connect to host
s.connect((host, port))
 
send = "";
while send != "stop":
    send = input(": ")
    packet = send
    print("sending", packet) 
    s.send(packet.encode())
    

s.close()
