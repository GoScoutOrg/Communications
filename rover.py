import socket, select, queue

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
    readable, writable, exceptional = select.select(inputs, outputs, inputs)

    # loop through each queue and do the things
    for s in readable:
        if s is server:
            connection, addr = server.accept()
            print(addr, "just joined");
            connection.setblocking(0)
            inputs.append(connection)
            messageQueues[connection] = [queue.Queue(), 0]
        else:
            data = s.recv(1024)
            print("\n\nrecv: ", data)
            if data:
                messageQueues[s][0].put(data)
                messageQueues[s][1] += 1
                if s not in outputs:
                    outputs.append(s)
            else:
                print(f"{s.getpeername()[0]} disconnected")
                if s in outputs:
                    outputs.remove(s)
                inputs.remove(s)
                s.close()
                del messageQueues[s]

    for s in writable:
        try:
            next_msg = messageQueues[s][0].get_nowait()
            seq = messageQueues[s][1]
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

