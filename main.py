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
system_ip = ""

def server_proc(q):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_data = (system_ip, 0) # Setting port = 0 lets os designate a port
    server.bind(server_data)

    server.listen()

    server_port = server.getsockname()[1]
    q.put(CommuncationPacket(False, True, COMMAND_SERVER_PORT, server_port))

    print("Server initialized: ", server)

    while True:
        client_connection, addr = server.accept()
        print("Incoming connection from ", addr)
        connections[addr] = client_connection

def client_proc(q):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
    client_data = (system_ip, 0)

    while q.empty():
        pass
    data = q.get()
    if data.isServer and data.command & COMMAND_SERVER_PORT == COMMAND_SERVER_PORT:
        client.connect((system_ip, data.data))

    # while True:
    #     pass
        # print(client.recv(1024))
        # print("reading")
        # https://docs.python.org/3/library/multiprocessing.html#multiprocessing.Queue.get
        # while q.empty():
        #     pass
        # data = q.get(False);
        # print(data)

def main() -> None:
    if (len(sys.argv) - 1 <= 0):
        return
    args = sys.argv[1:]

    system_ip = args[0];
    print("Initializing system IP: ", system_ip)

    q = Queue();

    server = Process(target=server_proc, args=(q,))
    client = Process(target=client_proc, args=(q,))

    server.start()
    client.start()

    server.join()
    client.join()
    return

if __name__ == "__main__":
    main();
