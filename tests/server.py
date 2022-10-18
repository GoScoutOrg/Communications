import socket 
import struct
 
# initializing socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname() 
port = 12345

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

