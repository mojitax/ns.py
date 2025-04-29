"""
Implements a wireless network adapter with a propagation delay. There is no need
to model a limited network capacity on this network adapter, since such a
capacity limit can be modeled using an upstream port or server element in
the network.
"""
import random

import simpy


class WirelessAdapter:
    """ Implements a wireless network adapter that introduces a propagation delay.
        Set the "out" member variable to the entity to receive the packet.

        Parameters
        ----------
        env: simpy.Environment
            the simulation environment.
        delay_dist: function
            a no-parameter function that returns the successive propagation
            delays on this wire.
        loss_dist: function
            a function that takes one optional parameter, which is the packet ID, and
            returns the loss rate.
    """

    def __init__(self,
                 env,
                 delay_dist,
                 owner,
                 loss_dist=None,
                 wireless_id=0,
                 debug=False):
        self.store = simpy.Store(env)
        self.delay_dist = delay_dist
        self.loss_dist = loss_dist
        self.owner = owner
        self.env = env
        self.wireless_id = wireless_id
        self.out = None
        self.packets_rec = 0
        self.debug = debug
        self.action = env.process(self.run())

    def run(self):
        """The generator function used in simulations."""
        while True:
            packet = yield self.store.get()
            for output in self.out:
                output.receive(packet)

    def put(self, packet):
        print(f"Wireless adapter #{self.wireless_id} received packet {packet.packet_id} at {self.env.now:.3f}")
        if self.delay_dist is not None:
            delay = self.delay_dist()
            yield self.env.timeout(delay)
        """ Sends a packet to this element. """
        self.packets_rec += 1
        if self.debug:
            print(f"Entered wireless #{self.wireless_id} at {self.env.now}: {packet}")

        packet.current_time = self.env.now
        return self.store.put(packet)
    def receive(self, packet):
        if self.loss_dist is None or random.uniform(
                0, 1) >= self.loss_dist(packet_id=packet.packet_id):
            # The amount of time for this packet to stay in my store
            queued_time = self.env.now - packet.current_time
            delay = self.delay_dist()
            # If queued time for this packet is greater than its propagation delay,
            # it implies that the previous packet had experienced a longer delay.
            # Since out-of-order delivery is not supported in simulation, deliver
            # to the next component immediately.
            if queued_time < delay:
                yield self.env.timeout(delay - queued_time)
            self.owner.put(packet)
            if self.debug:
                print(f"Packet received at wireless #{self.wireless_id} at {self.env.now}: {packet}")
        else:
            if self.debug:
                print(f"Dropped on adapter #{self.wireless_id} at "
                f"{self.env.now:.3f}: {packet}")
        
        

