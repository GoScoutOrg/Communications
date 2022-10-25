#from email import header
import socket
import struct

#construct the header

class GSPacket:
    def __init__(self,
                flag,
                SEQnum,
                src_ID,
                dest_ID,
                data
                #size is not needed because of python functionality??
                 
                 ):
        #connection, 
        self.flag = flag
        self.SEQnum = SEQnum
        self.src_ID = src_ID
        self.dest_ID = dest_ID
        self.data = data
        self.raw = None
    #return

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
    

def assemble_tcp_fields(self):
    self.raw = struct.pack('!HHLLBBHHH', # Data Structure Representation
    self.tcp_src,   # Source IP
    self.tcp_dst,    # Destination IP
    self.tcp_seq,    # Sequence
    self.tcp_ack_seq,  # Acknownlegment Sequence
    self.tcp_hdr_len,   # Header Length
    self.tcp_flags ,    # TCP Flags
    self.tcp_wdw,   # TCP Windows
    self.tcp_chksum,  # TCP cheksum
    self.tcp_urg_ptr # TCP Urgent Pointer
    )

    self.calculate_chksum() # Call Calculate CheckSum
    return

        