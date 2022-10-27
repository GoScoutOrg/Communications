#from email import header
import socket
import struct

#construct the header

class GSPacket:
    def __init__(self,
                tcp_flags,
                tcp_src, 
                tcp_dest,
                tcp_seq,
                tcp_ack_seq,
                tcp_hdr_len,
                data
                ):

        self.tcp_flags = tcp_flags    # TCP Flags
        self.tcp_src = tcp_src   # Source IP
        self.tcp_dst = tcp_dest    # Destination IP
        self.tcp_seq = tcp_seq    # Sequence
        self.tcp_ack_seq = tcp_ack_seq  # Acknownlegment Sequence
        self.tcp_hdr_len = tcp_hdr_len   # Header Length
        self.data = data,
        self.checksum = None
    #return


# def assemble_tcp_fields(GSpacket):
#     raw = struct.pack('IssIIIs', # Data Structure Representation
        
#         GSpacket.tcp_flags,    # TCP Flags
#         GSpacket.tcp_src,   # Source IP
#         GSpacket.tcp_dst,    # Destination IP
#         GSpacket.tcp_seq,    # Sequence
#         GSpacket.tcp_ack_seq,  # Acknownlegment Sequence
#         GSpacket.tcp_hdr_len,   # Header Length
#         GSpacket.data,
#         hash(GSpacket),  # TCP cheksum
#     )   

#     return raw

 

def send_a_string(GSpacket):
    data_to_send = str(GSpacket.tcp_flags) + "+" + str(GSpacket.tcp_src) + "+" + str(GSpacket.tcp_dst) + "+" + str(GSpacket.tcp_seq) + "+" + str(GSpacket.tcp_ack_seq) + "+" + str(GSpacket.tcp_hdr_len) + "+"  + str(GSpacket.data) + "+" + str(hash(GSpacket))
    print(data_to_send)

# def build(self):
#     packet = struct.pack(
#         self.src_port,  # Source Port
#         self.dst_port,  # Destination Port
#         0,              # Sequence Number
#         0,              # Acknoledgement Number
#         5 << 4,         # Data Offset
#         self.flags,     # Flags
#         0,              # Checksum (initial value)
#     )
#     return
    

def main():
    new_packet = GSPacket(1, "192.168.5.0".encode(), "192.168.4.0".encode(), 1, 1, 1, "hi".encode)
    send_a_string(new_packet)

    #print(pack_packet)
    #print(pack_packet.)
    

if __name__ == "__main__":
    main()


        