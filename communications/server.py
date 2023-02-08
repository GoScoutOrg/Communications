import sys
import socket
import json

import communications.utils as utils

def server_proc(pipe, system_ip : str, port : int, function_set : dict) -> int:
    if not utils.checkFunctionValidity(function_set):
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
            return utils.RETURN_ERROR

    while True:
        try:
            data = client_connection.recv(utils.BUFFER_SIZE)
            if data:
                packet = json.loads(data.decode("utf-8"))
                func_to_run = function_set.get(packet.get("FLAG"))
                args = packet.get("ARGS") #args MUST be a list of the desired args
                if func_to_run and args:
                    func_to_run(args)
                else:
                    flag = packet.get("FLAG")
                    args = packet.get("ARGS")
                    print(f"INVALID FUNCTION: {flag} : {args} in function set: {function_set}")
                    server.close()
                    return utils.RETURN_ERROR
        except (ConnectionRefusedError, TimeoutError):
            server.close()
            return utils.RETURN_ERROR

