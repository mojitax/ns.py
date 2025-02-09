from .packet import Packet

class ABE_Packet(Packet):
    """
    ABE_Packet extends the Packet class by adding additional fields related to 
    encryption and security mechanisms.
    
    Parameters
    ----------
    packet: Packet
        The original packet from which data is copied.
    abe_encryption: bool
        Indicates whether ABE encryption is applied.
    security_level: str
        Defines the security level (e.g., "low", "medium", "high").
    """

    def __init__(self, packet: Packet, attr_num: int = 0, security_level: int = 0):
        super().__init__(
            time=packet.time,
            size=packet.size,
            packet_id=packet.packet_id,
            realtime=packet.realtime,
            last_ack_time=packet.delivered_time,
            delivered=packet.delivered,
            src=packet.src,
            dst=packet.dst,
            flow_id=packet.flow_id,
            payload=packet.payload,
            tx_in_flight=packet.tx_in_flight,
            encrypted=packet.encrypted
        )
        self.attr_num = attr_num
        self.security_level = security_level

    def __repr__(self):
        return (super().__repr__() + 
                f", ABE_Encryption, attributes: {self.attr_num}, Security_Level: {self.security_level} bits, packet id: {self.packet_id}")

