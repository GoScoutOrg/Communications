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
    seq = 0
    ack = 0

    # connect to host
    s.connect((dst_ip, serverPort))

    # Hello!
    packet = PDU.GSPacket(PDU.FlagConstants.HELLO, src_ip, dst_ip, seq, ack, 0).compress()
    s.send(packet)
    seq += 1

    while True:
        sleep(1)
        packet = PDU.GSPacket(PDU.FlagConstants.HEARTBEAT, src_ip, dst_ip, seq, ack, 0).compress()
        seq += 1
        s.send(packet)

        recv = s.recv(1024)
        packet = PDU.decompress(recv)
        print(packet)

    s.close()


if __name__ == "__main__":
    main()
