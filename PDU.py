import socket
import struct

class FlagConstants:
    HELLO = 0x0
    HEARTBEAT = 0x1
    MOVE = 0x2
    ROTATE = 0x3

class GSPacket:
    def __init__(self,
                flags,
                src_ip, 
                dst_ip,
                seq,
                ack,
                payload_len,
                data = None
                ):
        self.flags = flags    # TCP Flags (uint8_t)
        self.src_ip = src_ip   # Source IP (uint8_t * 4)
        self.dst_ip = dst_ip    # dst_ipination IP (uint8_t * 4)
        self.seq = seq    # Sequence (uint32_t)
        self.ack = ack  # Acknownlegment Sequence (uint32_t)
        self.payload_len = payload_len   # Payload Length (uint32_t)
        self.data = data                # Data (max up to 1024 Bytes)

    def __repr__(self):
        ret = []
        ret.append("\n---------------")
        ret.append(f"FLAGS: {self.flags}")
        ret.append(f"SRC: {self.src_ip}")
        ret.append(f"DST: {self.dst_ip}")
        ret.append(f"SEQ: {self.seq}")
        ret.append(f"ACK: {self.ack}")
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
        seq = struct.pack("I", self.seq)
        ack = struct.pack("I", self.ack)
        payload_len = struct.pack("I", self.payload_len)
        if (self.payload_len == 0):
            return flags + src_ip + dst_ip + seq + ack + payload_len
        data = bytes(self.data, "ascii")
        return flags + src_ip + dst_ip + seq + ack + payload_len + data

def decompress(packet):
    flags = packet[0]
    src_ip = ".".join( [ str(x) for x in packet[1:5] ])
    dst_ip = ".".join( [ str(x) for x in packet[5:9] ])
    seq = int.from_bytes(packet[9:13], "little")
    ack = int.from_bytes(packet[13:17], "little")
    payload_len = int.from_bytes(packet[17:21], "little")
    if (payload_len == 0):
        return GSPacket(flags, src_ip, dst_ip, seq, ack, payload_len)
    data = packet[21:]
    return GSPacket(flags, src_ip, dst_ip, seq, ack, payload_len, data)

