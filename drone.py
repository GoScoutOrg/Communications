import socket
import PDU

# initize sockets and connection
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# host = '192.168.4.1'
host = "0.0.0.0" # for testing only

serverPort = 7777

# connect to host
s.connect((host, serverPort))

data = "";
while data != "stop":

    data = input(": ")
    if not data:
        continue

    packet = PDU.GSPacket(1, "192.168.5.0", "192.168.4.0", 1, 1, 1, data)
    strPacket = packet.convertToString();
    print("sending", strPacket) 
    s.send(strPacket.encode())

    recv = s.recv(1024);
    print("recv", recv)
    
s.close()

