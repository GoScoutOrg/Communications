import socket
import struct

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
port = 12345

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
