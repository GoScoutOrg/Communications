import socket 
import struct
 
# initializing socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '192.168.4.1'
serverPort = 7777
clientPort = 7778

# binding port and host
s.bind((host, serverPort))  
 
# waiting for a client to connect
s.listen(5) # 5 means that the server can deal with 5 connections. We only need 3

#Blocking
connection, addr = s.accept()
print ('Connection from', addr)
        
while True:
    recv = connection.recv(1024).decode()
    print(connection, recv)

