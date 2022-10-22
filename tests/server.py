import socket 
import struct
 
# initializing socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# host = socket.gethostname() 
# host = '0.0.0.0'
host = '192.168.4.1'
# print(socket.gethostbyname(socket.gethostname()))
port = 7777

print(socket.gethostbyname(host))

print(host, port)

# binding port and host
s.bind((host, port))  
 
# waiting for a client to connect
s.listen(5) 

#Blocking
connection, addr = s.accept()
print ('Connection from', addr)
        
while True:
    recv = connection.recv(1024).decode()
    print(connection, recv)

