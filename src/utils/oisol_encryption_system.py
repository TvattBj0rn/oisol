import base64
import os
import zlib

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


class AesGcm:
    def __init__(self):
        self._iv = os.urandom(12)
        self._key = os.getenv('ENCRYPTION_KEY').encode()
        self._ciphers = {}

    def _aes_encrypt(self, plain_text: bytes) -> str:
        cipher_encryptor = Cipher(
            algorithms.AES(self._key),
            modes.GCM(self._iv),
            backend=default_backend(),
        ).encryptor()

        ciphertext = base64.b64encode(cipher_encryptor.update(plain_text) + cipher_encryptor.finalize()).decode()

        self._ciphers[ciphertext] = cipher_encryptor.tag

        return ciphertext

    def _aes_decrypt(self, ciphertext: bytes, tag: bytes) -> bytes:
        cipher_decryptor = Cipher(
            algorithms.AES(self._key),
            modes.GCM(self._iv, tag),
            backend=default_backend(),
        ).decryptor()

        return cipher_decryptor.update(ciphertext) + cipher_decryptor.finalize()

    def encipher_process(self, plain_text: str) -> str:
        return self._aes_encrypt(zlib.compress(plain_text.encode()))

    def decipher_process(self, ciphertext: str) -> str:
        return zlib.decompress(self._aes_decrypt(
            base64.b64decode(ciphertext.encode()),
            self._ciphers.pop(ciphertext),
        )).decode()
