from ns.packet.packet import Packet


class SymPacket(Packet):
   
    def __init__(
        self,
        time,
        size,
        packet_id,
        realtime=0,
        last_ack_time=0,
        delivered=-1,
        src="source",
        dst="destination",
        flow_id=0,
        payload=None,
        tx_in_flight=-1,
        encrypted=False,
        parent_id=None,
    ):
        super().__init__(
            time,
            size,
            packet_id,
            realtime,
            last_ack_time,
            delivered,
            src,
            dst,
            flow_id,
            payload,
            tx_in_flight,
            encrypted,
        )
        self.parent_id = parent_id

    def __repr__(self):
        return f"id: {self.packet_id}, src: {self.src}, time: {self.time}, size: {self.size}"
