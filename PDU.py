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
                data,
                checksum = None
                ):
        self.tcp_flags = tcp_flags    # TCP Flags
        self.tcp_src = tcp_src   # Source IP
        self.tcp_dst = tcp_dest    # Destination IP
        self.tcp_seq = tcp_seq    # Sequence
        self.tcp_ack_seq = tcp_ack_seq  # Acknownlegment Sequence
        self.tcp_hdr_len = tcp_hdr_len   # Header Length
        self.data = data
        self.checksum = checksum

    def __repr__(self):
        data_to_send = str(self.tcp_flags) + "+" + str(self.tcp_src) + "+" + \
            str(self.tcp_dst) + "+" + str(self.tcp_seq) + "+" + \
            str(self.tcp_ack_seq) + "+" + str(self.tcp_hdr_len) + "+"  + \
            str(self.data) + "+" + str(self.checksum)
        return data_to_send

    def checkChecksum(self):
        saveChecksum = self.checksum;
        self.checksum = None;
        ret = self.checksum == hash(self)
        self.checksum = saveChecksum
        return ret;
    
    def convertToString(self):
        data_to_send = str(self.tcp_flags) + "+" + str(self.tcp_src) + "+" + \
            str(self.tcp_dst) + "+" + str(self.tcp_seq) + "+" + \
            str(self.tcp_ack_seq) + "+" + str(self.tcp_hdr_len) + "+"  + \
            str(self.data) + "+" + str(hash(self))
        return data_to_send

def unpackString(s):
    line = s.split("+")
    return GSPacket(line[0], line[1], line[2], line[3], line[4], line[5], line[6], line[7])


