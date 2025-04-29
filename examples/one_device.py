"""
A basic example that connects two packet generators to a network wire with
a propagation delay distribution, and then to a packet sink.
"""

from functools import partial
import random
from random import expovariate

import simpy
from ns.packet.device_receiver import DeviceReceiver
from ns.packet.dist_generator import DistPacketGenerator
from ns.packet.sink import PacketSink
from ns.port.wire import Wire
from ns.packet.device import Device
from ns.packet.aes_encrypt import AESEncrypt
from ns.packet.abe_encrypt import ABEEncrypt
from ns.port.wireless_adapter import WirelessAdapter

def arrival():
    return random.gauss(1, 0.02)


def packet_size():
    return int(expovariate(0.01))


env = simpy.Environment()

ps = DeviceReceiver(env, "device_1", arrival, packet_size, flow_id=0, encryption=ABEEncrypt(env), sym_encryption=AESEncrypt(env), sym_packets=3, debug=True)
ps2 = PacketSink(env, rec_flow_ids=False, debug=True)
pg1 = Device(env, "device", arrival, packet_size, flow_id=0, encryption=ABEEncrypt(env), sym_encryption=AESEncrypt(env), sym_packets=3, debug=True)

wireless = WirelessAdapter(env, None, wireless_id=1, debug=True, owner = pg1)
wireless1 = WirelessAdapter(env, partial(random.gauss, 0.1, 0.02), wireless_id=2, debug=False, owner = ps)
wireless2 = WirelessAdapter(env, partial(random.gauss, 0.1, 0.02), wireless_id=3, debug=False, owner = ps2)
pg1.out = wireless
wireless.out = [wireless1, wireless2]


env.run(until=100)

print(
    "ps - receiver packet delays: "
    + ", ".join(["{:.2f}".format(x) for x in ps.waits["device_1"]])
)

print(
    "Packet arrival times in ps: "
    + ", ".join(["{:.2f}".format(x) for x in ps.arrivals["device_1"]])
)
print(
    "packetsink - ps2 packet delays: "
    + ", ".join(["{:.2f}".format(x) for x in ps2.waits["device"]])
)

print(
    "Packet arrival times in ps2 1: "
    + ", ".join(["{:.2f}".format(x) for x in ps2.arrivals["device"]])
)