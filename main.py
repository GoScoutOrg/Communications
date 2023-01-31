import sys 
import socket
import PDU
from multiprocessing import Process, Queue, Pipe
from time import sleep

USAGE = "Usage: python3 main.py [system ip] [connection ip] [port]"
BUFFER_SIZE = 1024

def socketToIP(s : socket.socket):
    return s.getpeername()[0]

def send_PDU(socket : socket.socket, flag, src_ip, payload):
    packet = None
    if flag == PDU.FlagConstants.EXECUTION.value:
        packet = PDU.GSPacket(PDU.FlagConstants.EXECUTION.value, src_ip, socketToIP(socket), 0).compress()
    elif flag == PDU.FlagConstants.ACK.value:
        packet = PDU.GSPacket(PDU.FlagConstants.ACK.value, src_ip, socketToIP(socket), 0).compress()
    elif flag == PDU.FlagConstants.LOCATION.value:
        packet = PDU.GSPacket(PDU.FlagConstants.LOCATION.value, src_ip, socketToIP(socket), 9, payload).compress()
    elif flag == PDU.FlagConstants.CLOSE.value: #In this case wait for a recv and then close?
        packet = PDU.GSPacket(PDU.FlagConstants.CLOSE.value, src_ip, socketToIP(socket), 0).compress()

    if packet:
        socket.send(packet)
        print("Sent a PDU with flag:", flag,  "src_ip:", src_ip, "payload", payload )
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

def checkFunctionValidity(function_set) -> bool:
    # Check to see that the function set has at least 1 key
    return len(function_set.keys()) >= 1

def server_proc(pipe, system_ip : str, port : int, function_set : dict) -> int:
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
        # data = pipe.recv()
        # if data:
        #     print(data)
        #     break
        data = client_connection.recv(BUFFER_SIZE)
        if data:
            print(data)
            # packet = PDU.decompress(data)
            # print("RECV", packet)
            # print(data)
            # break
    return RETURN_SUCCESS


def client_proc(pipe, connect_ip : str, port : int, function_set : dict) -> int:
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
    while True:
        pipe_data = pipe.recv()
        if pipe_data:
            flag = pipe_data[ 0 ]
            data = pipe_data[ 1 ]
            # send_PDU(client, PDU.FlagConstants.LOCATION.value, connect_ip, gps_info)
            client.send(b'hello, world! From client')
            print(flag,data)
            # break
    #FOR PDU SEND TESTING PURPOSES
    # gps_info = "gps info\n"
    # send_PDU(client, PDU.FlagConstants.LOCATION.value, connect_ip, gps_info)
    #
    #
    # client.send(b'hello, world! From client')
    return RETURN_SUCCESS

# is_initialized = False
server_parent_end, server_child_end = Pipe()
client_parent_end, client_child_end = Pipe()
def parent_proc(system_ip : str, system_port : int, connection_ip : str, connection_port : int, function_set : dict) -> None:
    print("Initializing system network: ", system_ip, system_port)
    print("Initializing connection network: ", connection_ip, connection_port)

    server = Process(target=server_proc, args=(server_child_end, system_ip, system_port, function_set), daemon=True)
    client = Process(target=client_proc, args=(client_child_end, connection_ip, connection_port, function_set), daemon=True)

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
def open_communications(system_ip : str, system_port : int, connection_ip : str, connection_port : int, function_set : dict):
    # if is_initialized:
    #     sys.exit("Communications already initialized")
    # communications = Process(target=parent_proc, args=(system_ip, system_port, connection_ip, connection_port, function_set))
    # communications.start()
    return 

def send_packet(flag : str, data : str):
    # if not is_initialized:
    #     sys.exit("Communications NOT Initialized. Please call open_communications function before")
    client_parent_end.send((flag, data))

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
        "GPS": lambda : print("GPS"),
    }

    communications = Process(target=parent_proc, args=(system_ip, system_port, connect_ip, client_port, function_set))
    communications.start()

    sleep(10)
    send_packet("GPS", "192:145")

    communications.join()

    return

if __name__ == "__main__":
    main()
