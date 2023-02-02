import sys
import socket
import json

import communications.utils as utils

def client_proc(pipe, connect_ip : str, port : int, function_set : dict) -> int:
    if not utils.checkFunctionValidity(function_set):
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
            return utils.RETURN_ERROR
        except ConnectionRefusedError:
            pass
    while True:
        try:
            pipe_data = pipe.recv()
            if pipe_data:
                sending_data = json.dumps(pipe_data)
                client.send(bytes(sending_data,encoding="utf-8"))
        except KeyboardInterrupt:
            client.close();
            return utils.RETURN_ERROR
        except ConnectionRefusedError:
            pass
