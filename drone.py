import socket, queue
from time import sleep

import PDU

def main():
    # initize sockets and connection
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # dst_ip = '192.168.4.1'
    dst_ip = "0.0.0.0" # for testing only

    src_ip = socket.gethostbyname(socket.gethostname())

    serverPort = 7777

    messageQueues = queue.Queue()

    # connect to host
    s.connect((dst_ip, serverPort))

    # Hello!
    flag = PDU.FlagConstants.VOID
    while flag != PDU.FlagConstants.HELLO.value:
        sleep(1)
        packet = PDU.GSPacket(PDU.FlagConstants.HELLO.value, src_ip, dst_ip, 0).compress()
        s.send(packet)
        data = s.recv(1024)
        if data:
            packet = PDU.decompress(packet)
            print(packet)
            flag = packet.flags

    print("Finished Hello!")

    while True:
        sleep(1)
        packet = PDU.GSPacket(PDU.FlagConstants.HEARTBEAT.value, src_ip, dst_ip, 0).compress()
        s.send(packet)
        data = s.recv(1024)
        if data:
            packet = PDU.decompress(packet)
            print(packet)
    s.close()


if __name__ == "__main__":
    main()
