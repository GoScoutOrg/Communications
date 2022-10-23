import socket

# initize sockets and connection
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# host = '192.168.4.1'
host = "0.0.0.0" # for testing only
serverPort = 7777

# connect to host
s.connect((host, serverPort))
 
send = "";
while send != "stop":
    send = input(": ")
    packet = send
    print("sending", packet) 
    s.send(packet.encode())

    recv = s.recv(1024);
    print("recv", recv)
    
s.close()

