import socket, select, queue
import PDU
import time, random, sys

def socketToIP(s):
    return s.getpeername()[0]

def main():
    # initializing socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # src_ip = "0.0.0.0" # for testing only
    src_ip = '192.168.4.10'
    serverPort = 7777

    server.setblocking(0) #force the system to not block the calls

    # binding port and host
    server.bind((src_ip, serverPort))  

    # waiting for a client to connect
    server.listen(2) # 2 means that the server can deal with 2 connections. We only need 2 for now

    inputs = [server]
    outputs = []
    messageQueues = {}
    haltExecution = False

    while inputs:
        # time.sleep(random.randint(1, 4))
        time.sleep(1)
        # This thing takes a file discriptor
        readable, writable, exceptional = select.select(inputs, outputs, [])

        # loop through each queue and do the things
        for s in readable:
            if s is server:
                connection, addr = server.accept()
                print(connection)
                print(addr, "just joined")
                connection.setblocking(0)
                inputs.append(connection)
                if not messageQueues.get(socketToIP(connection)):
                    messageQueues[socketToIP(connection)] = queue.Queue()
            else:
                try:
                    data = s.recv(1024)
                except socket.error as e: 
                    time.sleep(3)
                    try:
                        data = s.recv(1024)
                    except socket.error as e: 
                        print("Agent Drone disconnected")
                        if s in outputs:
                            outputs.remove(s)
                        inputs.remove(s)
                        s.close()
                    
                    # sys.exit(1) 
                if data:
                    packet = PDU.decompress(data)
                    messageQueues[socketToIP(s)].put(packet)
                    if s not in outputs:
                        outputs.append(s)
                    flag = packet.flags
                    if flag == PDU.FlagConstants.MOVE.value or flag == PDU.FlagConstants.ROTATE.value: 
                        haltExecution = True
                    elif flag == PDU.FlagConstants.HEARTBEAT.value:
                        haltExecution = False
                    print("RECV", packet, haltExecution)
                else:
                    print("it hit THE spot")
                    

        for s in writable:
            try:
                next_msg = messageQueues[socketToIP(s)].get_nowait()
            except queue.Empty:
                outputs.remove(s)
            else:
                packet = None
                flag = next_msg.flags
                if flag == PDU.FlagConstants.HELLO.value:
                    packet = PDU.GSPacket(PDU.FlagConstants.HELLO.value, src_ip, socketToIP(s), 0).compress()
                elif flag == PDU.FlagConstants.HEARTBEAT.value:
                    packet = PDU.GSPacket(PDU.FlagConstants.HEARTBEAT.value, src_ip, socketToIP(s), 0).compress()
                elif flag == PDU.FlagConstants.MOVE.value or flag == PDU.FlagConstants.ROTATE.value: 
                    packet = PDU.GSPacket(PDU.FlagConstants.ACK.value, src_ip, socketToIP(s), 0).compress()

                if packet:
                    s.send(packet)
                else:
                    print("no valid packet")

if __name__ == "__main__":
    main()
