from PDU.py import *
#import PDU.py

def main():
    new_packet = GSPacket(1, 2, 3, 4, 5, 6, "hello")
    pack_packet = assemble_tcp_fields(new_packet)

    print(pack_packet)
    

if __name__ == "__main__":
    main()