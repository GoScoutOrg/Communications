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
        self.data = data
        self.checksum = None

    def checksum(self):
        return self.checksum == hash(self)
    
    def convertToString(self):
        data_to_send = str(self.tcp_flags) + "+" + str(self.tcp_src) + "+" + \
            str(self.tcp_dst) + "+" + str(self.tcp_seq) + "+" + \
            str(self.tcp_ack_seq) + "+" + str(self.tcp_hdr_len) + "+"  + \
            str(self.data) + "+" + str(hash(self))
        return data_to_send

def unpackString(s):
    line = s.split("+")
    return GSPacket(s[0], s[1], s[2], s[3], s[4], s[5], s[6])


