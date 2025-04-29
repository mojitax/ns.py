from ns.packet.aes_packet import AES_Packet
from ns.packet.packet import Packet
from ns.packet.crypto_module import CryptoModule
from ns.packet.sym_packet import SymPacket

class Device:


    def __init__(
        self,
        env,
        element_id,
        arrival_dist,
        size_dist,
        initial_delay=0,
        finish=None,
        size=None,
        flow_id=0,
        rec_flow=False,
        debug=False,
        encryption: CryptoModule = None,
        sym_encryption: CryptoModule = None,
        sym_packets: int = 0,
    ):
        self.element_id = element_id
        self.env = env
        self.arrival_dist = arrival_dist
        self.size_dist = size_dist
        self.initial_delay = initial_delay
        self.finish = float("inf") if finish == None else finish
        self.size = float("inf") if size == None else size
        self.out = None
        self.packets_sent = 0
        self.sent_size = 0
        self.action = env.process(self.run())
        self.flow_id = flow_id
        self.encryption = encryption
        self.rec_flow = rec_flow
        self.time_rec = []
        self.size_rec = []
        self.debug = debug
        self.sym_encryption = sym_encryption
        self.sym_packets = sym_packets

    def run(self):
        yield self.env.timeout(self.initial_delay)

        while self.env.now < self.finish and self.sent_size < self.size:
            packet = Packet(
                self.env.now,
                self.size_dist(),
                self.packets_sent,
                src=self.element_id,
                flow_id=self.flow_id,
            )
            yield self.env.process(self.encryption.encrypt(packet))
            self.out.put(packet)

            self.packets_sent += 1
            self.sent_size += packet.size
            
            if self.rec_flow:
                self.time_rec.append(packet.time)
                self.size_rec.append(packet.size)

            if self.debug:
                print(
                    f"Device {self.element_id} sent ASYMMETRIC packet {packet.packet_id}"
                    f" with size {packet.size}, "
                    f"flow_id {packet.flow_id} at time {self.env.now:.4f}."
                )
            for i in range(self.sym_packets):
                if self.debug:    
                    print(
                    f"Symmetric packet no. {i} out of {self.sym_packets}"
                    )
                sym_packet = Packet(
                    self.env.now,
                    self.size_dist(),
                    self.packets_sent,
                )
                aes_packet = AES_Packet(sym_packet, key_packet_id=packet.packet_id, pack_num=i, all_packets=self.sym_packets)
                yield self.env.process(self.sym_encryption.encrypt(aes_packet))               
                self.out.put(aes_packet)

                self.packets_sent += 1
                self.sent_size += packet.size
                
                if self.rec_flow:
                    self.time_rec.append(aes_packet.time)
                    self.size_rec.append(aes_packet.size)

                if self.debug:
                    print(
                        f"Device {self.element_id} sent SYMMETRIC packet {aes_packet.packet_id}"
                        f" with size {aes_packet.size}, with parent {aes_packet.key_packet_id} "
                        f" packet no. {aes_packet.pack_num + 1} out of {aes_packet.all_packets}, "
                        f"flow_id {aes_packet.flow_id} at time {self.env.now:.4f}."
                    )
            

            # waits for the next transmission
            yield self.env.timeout(self.arrival_dist())
