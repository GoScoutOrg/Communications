import sys, os, signal
import socket
from time import sleep
import PDU
from collections.abc import Callable
from multiprocessing import Process, Queue

USAGE = "Usage: python3 main.py [system ip] [connection ip] [port]"
BUFFER_SIZE = 1024

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
    elif flag == PDU.FlagConstants.CLOSE.value: #In this case wait for a recv and then close?
        packet = PDU.GSPacket(PDU.FlagConstants.CLOSE.value, src_ip, socketToIP(socket), 0).compress()


    if packet:
        socket.send(packet)
    else:   
        print("no valid packet")
        return -1
    return

class ProcCommunicationPacket:
    def __init__(self, to_pid, from_pid, command):
        self.to_pid = to_pid
        self.from_pid = from_pid
        self.command = command

COMMAND_ERROR = 0x1

RETURN_SUCCESS = 0x0
RETURN_ERROR = 0x1

def checkFunctionValidity(function_set : dict[str, Callable]) -> bool:
    # Check to see that the function set has at least 1 key
    return len(function_set.keys()) >= 1

def server_proc(q : Queue, system_ip : str, port : int, function_set : dict) -> int:
    if not checkFunctionValidity(function_set):
        sys.exit("SERVER: function validity error")

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # check and turn on TCP Keepalive
    x = server.getsockopt( socket.SOL_SOCKET, socket.SO_KEEPALIVE)
    if(x == 0):
        x = server.setsockopt( socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)

    server_data = (system_ip, port) # Setting port = 0 lets os designate a port
    server.bind(server_data)

    server.listen()

    print("SERVER:\tinitialized: ", server)

    client_connection = addr = socket.socket() #Initialize as an empty socket
    awaiting_connection = True
    while awaiting_connection:
        try:
            client_connection, addr = server.accept()
            print("SERVER:\tIncoming connection from ", addr)
            awaiting_connection = False
        except KeyboardInterrupt:
            server.close()
            return RETURN_ERROR
    while True:
        data = client_connection.recv(BUFFER_SIZE)
        if data:
            print(data)
            break
    return RETURN_SUCCESS


def client_proc(q : Queue, connect_ip : str, port : int, function_set : dict) -> int:
    if not checkFunctionValidity(function_set):
        sys.exit("CLIENT: function validity error")

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    x = client.getsockopt( socket.SOL_SOCKET, socket.SO_KEEPALIVE)
    if(x == 0):
        x = client.setsockopt( socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)

    client_data = (connect_ip, port)
    print("CLIENT:\tInitialized: ", client)
    print("CLIENT:\tConnecting to: ", client_data)

    while True:
        try:
            client.connect(client_data)
            print("connected to the server")
            break
        except KeyboardInterrupt:
            client.close()
            return RETURN_ERROR
        except ConnectionRefusedError:
            pass

    client.send(b'hello, world! From client')
    return RETURN_SUCCESS

def parent_proc(system_ip : str, system_port : int, connection_ip : str, connection_port : int, function_set : dict) -> None:
    print("Initializing system network: ", system_ip, system_port)
    print("Initializing connection network: ", connection_ip, connection_port)

    q = Queue()

    server = Process(target=server_proc, args=(q, system_ip, system_port, function_set), daemon=True)
    client = Process(target=client_proc, args=(q, connection_ip, connection_port, function_set), daemon=True)

    server.start()
    client.start()

    clients_running = 0x0 # --> 0x11 = 0x01 | 0x10
    while clients_running != 0x11:
        client.join(timeout=1)
        if not client.is_alive():
            clients_running |= 0x01
        server.join(timeout=1)
        if not server.is_alive():
            clients_running |= 0x10
    return


# START API FUNCTIONS
coms = None;
class Communications:
    def __init__(self, system_ip : str, system_port : int, connection_ip : str, connection_port : int, function_set : dict):
        self.system_ip = system_ip;
        self.system_port = system_port
        self.connection_ip = connection_ip
        self.connection_port = connection_port
        self.function_set = function_set
        self.communiations = None
        self.running = False

    def start(self):
        self.running = True;
        coms = Process(target=parent_proc, args=(self.system_ip, self.system_port, self.connection_ip, self.connection_port, self.function_set))
        coms.start()
        # self.communications = Process(target=parent_proc, args=(self.system_ip, self.system_port, self.connection_ip, self.connection_port, self.function_set))
        # self.communications.start()
        # print(self.communications.pid)
        # self.communications.terminate();
        # self.communications.join();
        # self.communications.close();
        # self.communications.join(timeout=1)

    def stop(self):
        # signal.signal(signal.SIGTERM, self.communiations)
        # coms.terminate()
        # coms.close()
        # signal.signal(signal.SIGTERM, self.communications.pid)
        # print("stopping")
        # test = self.communications.pid
        # os.kill(test, signal.SIGTERM)
        # self.communications.terminate();
        # self.communications.join();
        # self.communications.close();


# communications = Process()
# test = 'hello'
# def open_communications(system_ip : str, system_port : int, connection_ip : str, connection_port : int, function_set : dict):
#     communications = Process(target=parent_proc, args=(system_ip, system_port, connection_ip, connection_port, function_set))
#     communications.start()
#     print(test)
#     return 
#
# def close_communications() -> None:
#     communications.terminate()
#     communications.close()
#     print(test)
# END API FUNCTIONS

def main() -> None:
    if (len(sys.argv) - 4 <= 0):
        sys.exit(USAGE)
    args = sys.argv[1:]

    system_ip = args[0]
    connect_ip = args[1]
    if len(system_ip.split('.')) != 4 or len(connect_ip.split('.')) != 4:
        sys.exit(USAGE)
    system_port = args[2]
    client_port = args[3]
    if not system_port.isnumeric() or not client_port.isnumeric():
        sys.exit(USAGE)
    else:
        system_port = int(system_port)
        client_port = int(client_port)
        if (system_port < 1024 or system_port > 49151) or (client_port < 1024 or client_port > 49151):
            sys.exit(USAGE)

    function_set = {
        "MOVE": lambda : print("MOVE"),
        "ROTATE": lambda : print("ROTATE"),
    }

    coms = Communications(system_ip, system_port, connect_ip, client_port, function_set)
    coms.start()
    sleep(1)
    coms.stop()
    # coms.stop()
    # coms = open_communications(system_ip, system_port, connect_ip, client_port, function_set)
    # print(coms)
    # sleep(2)
    # close_communications()

    return

if __name__ == "__main__":
    main()
