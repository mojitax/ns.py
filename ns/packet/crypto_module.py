from abc import ABC, abstractmethod

class CryptoModule(ABC):
    def __init__(self, env):
        self.env = env

    @abstractmethod
    def encrypt(self, data: bytes) -> bytes:
        pass

    @abstractmethod
    def decrypt(self, data: bytes) -> bytes:
        pass
