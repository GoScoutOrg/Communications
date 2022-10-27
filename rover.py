import socket, select, queue
import PDU.py

# initializing socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '192.168.4.1'
# host = "0.0.0.0" # for testing only
serverPort = 7777

server.setblocking(0) #force the system to not block the calls

# binding port and host
server.bind((host, serverPort))  

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
                messageQueues[connection.getpeername()[0]] = [queue.Queue(), 0]
        else:
            data = s.recv(1024)
            print("\n\nrecv: ", data)
            if data:
                messageQueues[s.getpeername()[0]][0].put(data)
                messageQueues[s.getpeername()[0]][1] += 1
                if s not in outputs:
                    outputs.append(s)
            else:
                print(f"{s.getpeername()[0]} disconnected")
                if s in outputs:
                    outputs.remove(s)
                inputs.remove(s)
                s.close()
                # del messageQueues[s.getpeername()[0]]

    for s in writable:
        try:
            next_msg = messageQueues[s.getpeername()[0]][0].get_nowait()
            seq = messageQueues[s.getpeername()[0]][1]
            print("queue: ", next_msg, seq)
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

