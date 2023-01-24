import sys
import socket
from multiprocessing import Process, Queue

class CommuncationPacket:
    def __init__(self, isRoot, isServer, command, data):
        self.isRoot = isRoot
        self.isServer = isServer
        self.command = command
        self.data = data

COMMAND_SERVER_PORT = 0x1

connections = {}

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

    while True:
        try:
            client_connection, addr = server.accept()
            print("Incoming connection from ", addr)
            connections[addr] = client_connection
        except KeyboardInterrupt:
            server.close()
            return

def client_proc(q, system_ip, connect_ip, port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    x = client.getsockopt( socket.SOL_SOCKET, socket.SO_KEEPALIVE)
    if(x == 0):
        x = client.setsockopt( socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)

    client_data = (connect_ip, port)
    # client.bind((system_ip, port))
    print("client initialized: ", client)

    while True:
        try:
            client.connect(client_data);
            # print("connected to the server")
            break
        except KeyboardInterrupt:
            client.close()
            return
        except ConnectionRefusedError:
            pass
#  while True:
    # try:
    #     s = "Hello?"
    #     print('sending')
    #     client.send(s.encode())
    # except KeyboardInterrupt:
    #     client.close()
    #     return


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
    port_a = args[2]
    port_b = args[3]
    if not port_a.isnumeric() or not port_b.isnumeric():
        print("Usage: python3 main.py [system ip] [connection ip] [port]")
        return
    else:
        port_a = int(port_a)
        port_b = int(port_b)
        if (port_a < 1024 or port_a > 49151) or (port_b < 1024 or port_b > 49151):
            print("Usage: python3 main.py [system ip] [connection ip] [port]")
            return

    print("Initializing system IP: ", system_ip)
    print("Initializing system port: ", port_a)
    print("Initializing connection IP: ", connect_ip)
    print("Initializing connection IP: ", port_b)

    q = Queue()

    server = Process(target=server_proc, args=(q, system_ip, connect_ip, port_a))
    client = Process(target=client_proc, args=(q, system_ip, connect_ip, port_b))

    server.start()
    client.start()

    server.join()
    print("server done")
    client.join()
    print("client done")

    print("done")

    return

if __name__ == "__main__":
    main()
