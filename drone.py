import socket
import time
import sys

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
        time.sleep(1)
        packet = PDU.GSPacket(PDU.FlagConstants.HELLO.value, src_ip, dst_ip, 0).compress()
        s.send(packet)
        print('sent hello')
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
    while True:
        time.sleep(1)

        if (flag == PDU.FlagConstants.HEARTBEAT.value or flag == PDU.FlagConstants.HELLO.value):
            packet = PDU.GSPacket(PDU.FlagConstants.HEARTBEAT.value, src_ip, dst_ip, 0).compress()

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
            packet = PDU.decompress(packet)
            flag = packet.flags
            print(packet)
    s.close()


if __name__ == "__main__":
    main()
