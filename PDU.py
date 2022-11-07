import socket
import struct
from enum import Flag

class FlagConstants(Flag):
    # For coding things nice
    VOID  = 0x0

    # Stable coms
    HELLO = 0x1
    HEARTBEAT = 0x2
    ACK = 0x3
    CLOSE = 0x4

    # Command flags
    MOVE = 0x5
    ROTATE = 0x6

class GSPacket:
    def __init__(self,
                flags,
                src_ip, 
                dst_ip,
                payload_len,
                data = None
                ):
        self.flags = flags    # TCP Flags (uint8_t)
        self.src_ip = src_ip   # Source IP (uint8_t * 4)
        self.dst_ip = dst_ip    # dst_ipination IP (uint8_t * 4)
        self.payload_len = payload_len   # Payload Length (uint32_t)
        self.data = data                # Data (max up to 1024 Bytes)

    def __repr__(self):
        ret = []
        ret.append("\n---------------")
        ret.append(f"FLAG: {FlagConstants(self.flags).name}")
        ret.append(f"SRC: {self.src_ip}")
        ret.append(f"DST: {self.dst_ip}")
        ret.append(f"PAYLOAD_LEN: {self.payload_len}")
        ret.append(f"DATA: {self.data}")
        ret.append("\n---------------")
        return "\n".join(ret)

    def packIp(self, ipString):
        ip = [ struct.pack("B", int(x.rjust(3, '0'))) for x in ipString.split(".") ]
        return ip[0] + ip[1] + ip[2] + ip[3]

    def compress(self):
        flags = struct.pack("B", self.flags)
        src_ip = self.packIp(self.src_ip)
        dst_ip = self.packIp(self.dst_ip)
        payload_len = struct.pack("I", self.payload_len)
        if (self.payload_len == 0):
            return flags + src_ip + dst_ip + payload_len
        data = bytes(self.data, "ascii")
        return flags + src_ip + dst_ip + payload_len + data

def decompress(packet):
    flags = packet[0]
    src_ip = ".".join( [ str(x) for x in packet[1:5] ])
    dst_ip = ".".join( [ str(x) for x in packet[5:9] ])
    payload_len = int.from_bytes(packet[9:13], "little")
    if (payload_len == 0):
        return GSPacket(flags, src_ip, dst_ip, payload_len)
    data = packet[13:]
    return GSPacket(flags, src_ip, dst_ip, payload_len, data)

