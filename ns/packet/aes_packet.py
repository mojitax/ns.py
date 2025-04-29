from .packet import Packet

class AES_Packet(Packet):
    def __init__(self, packet: Packet, key_packet_id: int = 0, pack_num: int = 0, all_packets: int = 0):
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
        self.key_packet_id = key_packet_id
        self.pack_num = pack_num
        self.all_packets = all_packets

    def __repr__(self):
        return (super().__repr__() + 
                f", AES_Encryption parent packet: {self.key_packet_id}, pack_num: {self.pack_num}, all_packets: {self.all_packets}")

