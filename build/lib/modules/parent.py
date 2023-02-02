import sys 
from multiprocessing import Process, Pipe

import utils
from server import server_proc
from client import client_proc

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
def send_packet(flag : str, data : list[str]):
    client_parent_end.send({"FLAG": flag, "ARGS": data})
# END API FUNCTIONS

def main() -> int:
    if (len(sys.argv) - 4 <= 0):
        sys.exit(utils.USAGE)
    args = sys.argv[1:]

    system_ip = args[0]
    connect_ip = args[1]
    if len(system_ip.split('.')) != 4 or len(connect_ip.split('.')) != 4:
        sys.exit(utils.USAGE)
    system_port = args[2]
    client_port = args[3]
    if not system_port.isnumeric() or not client_port.isnumeric():
        sys.exit(utils.USAGE)
    else:
        system_port = int(system_port)
        client_port = int(client_port)
        if (system_port < 1024 or system_port > 49151) or (client_port < 1024 or client_port > 49151):
            sys.exit(utils.USAGE)

    """
    Function set rules:
        all arguments to functions MUST be in the form of a list[str]. The function itself must parse the arguments!
    """
    function_set = {
        "GPS": lambda args : print("This is the GPS function"),
        "MOVE": lambda args : print(f"This is the MOVE function: x:{int(args[0])}, y:{int(args[1])}"),
    }

    communications = Process(target=parent_proc, args=(system_ip, system_port, connect_ip, client_port, function_set))
    communications.start()

    flag = ""
    while flag != "CLOSE":
        flag = input("\n\nInput flag ")
        args = input("\n\nInput args: ").split(' ')
        send_packet(flag, args)

    communications.join()
    return utils.RETURN_SUCCESS

if __name__ == "__main__":
    main()
