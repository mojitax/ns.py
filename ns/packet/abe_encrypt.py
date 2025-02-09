from ns.packet.abe_packet import ABE_Packet
from .crypto_module import CryptoModule
from .packet import Packet

class ABEEncrypt(CryptoModule):
    def encrypt(self, data: Packet) -> ABE_Packet:
        ABE_data = ABE_Packet(data)  # Cast packet to ABEPacket
        yield self.env.timeout(0.1) # Simulate encryption delay
        ABE_data.encrypted = True
        return ABE_data

    def decrypt(self, data: ABE_Packet) -> Packet:
        # Implement the decryption logic here
        pass
