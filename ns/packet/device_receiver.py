from ns.packet.aes_packet import AES_Packet
from ns.packet.device import Device
from ns.packet.packet import Packet
from ns.packet.crypto_module import CryptoModule
from collections import defaultdict as dd
import simpy
class DeviceReceiver(Device):
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
        rec_arrivals: bool = True,
        absolute_arrivals: bool = True,
        rec_waits: bool = True,
        rec_flow_ids: bool = True,
    ):
        super().__init__(
            env,
            element_id,
            arrival_dist,
            size_dist,
            initial_delay,
            finish,
            size,
            flow_id,
            rec_flow,
            debug,
            encryption,
            sym_encryption,
            sym_packets
        )
        self.store = simpy.Store(env)
        self.env = env
        self.rec_waits = rec_waits
        self.rec_flow_ids = rec_flow_ids
        self.rec_arrivals = rec_arrivals
        self.absolute_arrivals = absolute_arrivals
        self.waits = dd(list)
        self.arrivals = dd(list)
        self.packets_received = dd(lambda: 0)
        self.bytes_received = dd(lambda: 0)
        self.packet_sizes = dd(list)
        self.packet_times = dd(list)
        self.perhop_times = dd(list)
        self.arrivals = dd(list)

        self.first_arrival = dd(lambda: 0)
        self.last_arrival = dd(lambda: 0)


    def run(self):
        yield self.env.timeout(self.initial_delay)
        if self.out is not None:
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

                #if self.debug:
                print(
                    f"Device {self.element_id} sent ASYMMETRIC packet {packet.packet_id}"
                    f" with size {packet.size}, "
                    f"flow_id {packet.flow_id} at time {self.env.now:.4f}."
                )
                for i in range(self.sym_packets):
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

                    #if self.debug:
                    print(
                        f"Device {self.element_id} sent SYMMETRIC packet {aes_packet.packet_id}"
                        f" with size {aes_packet.size}, with parent {aes_packet.key_packet_id} "
                        f" packet no. {aes_packet.pack_num + 1} out of {aes_packet.all_packets}, "
                        f"flow_id {aes_packet.flow_id} at time {self.env.now:.4f}."
                    )


                # waits for the next transmission
                yield self.env.timeout(self.arrival_dist())
    def put(self, packet):
        """Sends a packet to this element."""
        now = self.env.now

        if self.rec_flow_ids:
            rec_index = packet.flow_id
        else:
            rec_index = packet.src

        if self.rec_waits:
            self.waits[rec_index].append(self.env.now - packet.time)
            self.packet_sizes[rec_index].append(packet.size)
            self.packet_times[rec_index].append(packet.time)
            self.perhop_times[rec_index].append(packet.perhop_time)

        if self.rec_arrivals:
            self.arrivals[rec_index].append(now)
            if len(self.arrivals[rec_index]) == 1:
                self.first_arrival[rec_index] = now

            if not self.absolute_arrivals:
                self.arrivals[rec_index][-1] = (
                    now - self.last_arrival[rec_index]
                )

            self.last_arrival[rec_index] = now

        if self.debug:
            print(
                f"At time {now:.2f}, packet {packet.packet_id} in "
                f"flow {packet.flow_id} arrived."
            )
            if self.rec_waits and len(self.packet_sizes[rec_index]) >= 10:
                bytes_received = sum(self.packet_sizes[rec_index][-9:])
                time_elapsed = self.env.now - (
                    self.packet_times[rec_index][-10]
                    + self.waits[rec_index][-10]
                )
                print(
                    f"Average throughput (last 10 packets): "
                    f"{(float(bytes_received) / time_elapsed):.2f} bytes/second."
                )

        self.packets_received[rec_index] += 1
        self.bytes_received[rec_index] += packet.size