import socket, select, queue
import PDU

def socketToIP(socket):
    return socket.getpeername()[0]

def main():
    # initializing socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # host = '192.168.4.1'
    src_ip = "0.0.0.0" # for testing only
    serverPort = 7777

    server.setblocking(0) #force the system to not block the calls

    # binding port and host
    server.bind((src_ip, serverPort))  

    # waiting for a client to connect
    server.listen(2) # 2 means that the server can deal with 2 connections. We only need 2 for now

    inputs = [server]
    outputs = []
    messageQueues = {}

    while inputs:
        # This thing takes a file discriptor
        readable, writable, exceptional = select.select(inputs, outputs, inputs)

        # loop through each queue and do the things
        for s in readable:
            if s is server:
                connection, addr = server.accept()
                print(connection)
                print(addr, "just joined")
                connection.setblocking(0)
                inputs.append(connection)
                if not messageQueues.get(connection.getpeername()[0]):
                    messageQueues[connection.getpeername()[0]] = [queue.Queue(), 0, 0]
            else:
                data = s.recv(1024)
                if data:
                    packet = PDU.decompress(data)
                    print("\n-------\n", packet, "\n-------\n")
                    messageQueues[socketToIP(s)][0].put(data)
                    messageQueues[socketToIP(s)][1] += 1
                    if s not in outputs:
                        outputs.append(s)
                else:
                    print(f"{socketToIP(s)} disconnected")
                    if s in outputs:
                        outputs.remove(s)
                    inputs.remove(s)
                    s.close()

        for s in writable:
            try:
                next_msg = messageQueues[socketToIP(s)][0].get_nowait()
                seq = messageQueues[socketToIP(s)][1]
                print("sending seq")
            except queue.Empty:
                outputs.remove(s)
            else:
                s.send(str(seq).encode())

        for s in exceptional:
            inputs.remove(s)
            if s in outputs:
                outputs.remove(s)
            s.close()
            del messageQueues[s]

if __name__ == "__main__":
    main()
