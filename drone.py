import socket
import time
import sys
import random

import PDU

def main():
    # initize sockets and connection
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2) # Time out tim

    # dst_ip = '192.168.4.1'
    dst_ip = "0.0.0.0" # for testing only

    src_ip = socket.gethostbyname(socket.gethostname())

    serverPort = 7777

    # connect to host
    while True:
        try: 
            s.connect((dst_ip, serverPort))
            break;
        except:
            continue;

    # Hello!
    flag = PDU.FlagConstants.VOID
    while flag != PDU.FlagConstants.HELLO.value:
        time.sleep(random.randint(1, 4))
        packet = PDU.GSPacket(PDU.FlagConstants.HELLO.value, src_ip, dst_ip, 0).compress()
        s.send(packet)
        try:
            data = s.recv(1024)
        except socket.timeout as e:
            if e.args[0] == 'timed out':
                continue
            else:
                sys.exit(1)
        except socket.error as e:
                sys.exit(1)
        else:
            packet = PDU.decompress(packet)
            print(packet)
            flag = packet.flags

    # Data Loop
    stopHeartbeat = False
    n = 0
    while True:
        time.sleep(random.randint(1, 10))

        packet = None
        if (n == 5):
            packet = PDU.GSPacket(PDU.FlagConstants.ROTATE.value, src_ip, dst_ip, 11, "HELLO WORLD").compress();
            n = 0
            stopHeartbeat = True;
        else:
            packet = PDU.GSPacket(PDU.FlagConstants.HEARTBEAT.value, src_ip, dst_ip, 0).compress()
            n+=1

        if packet:
            s.send(packet)

        flag = PDU.FlagConstants.VOID.value;
        packet = None

        try:
            data = s.recv(1024)
        except socket.timeout as e:
            if e.args[0] == 'timed out':
                print("time out")
                continue
            else:
                print("Error occured: ", e)
                sys.exit(1)
        except socket.error as e:
                print("Error occured: ", e)
                sys.exit(1)
        else:
            packet = PDU.decompress(data)
            flag = packet.flags
            if flag == PDU.FlagConstants.ACK.value:
                stopHeartbeat = False;
            print(packet)
    s.close()


if __name__ == "__main__":
    main()
