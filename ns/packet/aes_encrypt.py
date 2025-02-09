from ns.packet.aes_packet import AES_Packet
from ns.packet.crypto_module import CryptoModule
from .packet import Packet

class AESEncrypt(CryptoModule):
    def encrypt(self, data: Packet) -> AES_Packet:
        AES_data = AES_Packet(data)  # Cast packet to AESPacket
        yield self.env.timeout(0.01) # Simulate encryption delay
        AES_data.encrypted = True
        return AES_data

    def decrypt(self, data: AES_Packet) -> Packet:
        # Implement the decryption logic here
        pass
