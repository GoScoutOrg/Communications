import sys, os
import socket
import PDU
from multiprocessing import Process, Queue

BUFFER_SIZE = 1024

class CommuncationPacket:
    def __init__(self, to_pid, from_pid, command, data):
        self.to_pid = to_pid
        self.from_pid = from_pid
        self.command = command
        self.data = data

def server_proc(q, system_ip, connect_ip, port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # check and turn on TCP Keepalive
    x = server.getsockopt( socket.SOL_SOCKET, socket.SO_KEEPALIVE)
    if(x == 0):
        x = server.setsockopt( socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)

    server_data = (system_ip, port) # Setting port = 0 lets os designate a port
    server.bind(server_data)

    server.listen()

    print("Server initialized: ", server)

    client_connection = addr = socket.socket() #Initialize as an empty socket
    awaiting_connection = True
    while awaiting_connection:
        try:
            client_connection, addr = server.accept()
            print("Incoming connection from ", addr)
            awaiting_connection = False
        except KeyboardInterrupt:
            server.close()
            return
    while True:
        print("recving")
        data = client_connection.recv(BUFFER_SIZE)
        if data:
            print(data)
            break
    return


def client_proc(q, system_ip, connect_ip, port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    x = client.getsockopt( socket.SOL_SOCKET, socket.SO_KEEPALIVE)
    if(x == 0):
        x = client.setsockopt( socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)

    client_data = (connect_ip, port)
    # client.bind((system_ip, port))
    print("client initialized: ", client)
    print("connecting to: ", client_data)

    while True:
        try:
            client.connect(client_data)
            print("connected to the server")
            break
        except KeyboardInterrupt:
            client.close()
            return
        except ConnectionRefusedError:
            pass

    print("sending")
    client.send(b'hello, world! From client')
    return

def socketToIP(s):
    return s.getpeername()[0]

def send_PDU(socket, flag, src_ip):
    # grab GPS info 
    gps_info = "gps info\n"

    packet = None
    
    if flag == PDU.FlagConstants.EXECUTION.value:
        packet = PDU.GSPacket(PDU.FlagConstants.EXECUTION.value, src_ip, socketToIP(socket), 0).compress()
    elif flag == PDU.FlagConstants.ACK.value:
        packet = PDU.GSPacket(PDU.FlagConstants.ACK.value, src_ip, socketToIP(socket), 0).compress()
    elif flag == PDU.FlagConstants.LOCATION.value:
        packet = PDU.GSPacket(PDU.FlagConstants.LOCATION.value, src_ip, socketToIP(socket), 9, gps_info).compress()

    if packet:
        socket.send(packet)
    else:   
        print("no valid packet")
        return -1
    return


def main() -> None:
    if (len(sys.argv) - 4 <= 0):
        print("Usage: python3 main.py [system ip] [connection ip] [port]")
        return
    args = sys.argv[1:]

    system_ip = args[0]
    connect_ip = args[1]
    if len(system_ip.split('.')) != 4 or len(connect_ip.split('.')) != 4:
        print("Usage: python3 main.py [system ip] [connection ip] [port]")
        return
    system_port = args[2]
    client_port = args[3]
    if not system_port.isnumeric() or not client_port.isnumeric():
        print("Usage: python3 main.py [system ip] [connection ip] [port]")
        return
    else:
        system_port = int(system_port)
        client_port = int(client_port)
        if (system_port < 1024 or system_port > 49151) or (client_port < 1024 or client_port > 49151):
            print("Usage: python3 main.py [system ip] [connection ip] [port]")
            return

    print("Initializing system network: ", system_ip, system_port)
    print("Initializing connection network: ", connect_ip, client_port)

    q = Queue()

    server = Process(target=server_proc, args=(q, system_ip, connect_ip, system_port))
    client = Process(target=client_proc, args=(q, system_ip, connect_ip, client_port))

    server.start()
    client.start()

    while True:
        d = q.get()
        if d != None:
            print("got something")

    server.join()
    print("server done")
    client.join()
    print("client done")

    print("done")

    return

if __name__ == "__main__":
    main()
