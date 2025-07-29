import hashlib
from Crypto.Hash import keccak


class BloomFilter:
    def __init__(self, size: int = 2048):
        self.size = size
        self.bit_array = 0

    def _get_indexes(self, data: bytes):
        k = keccak.new(digest_bits=256)
        k.update(data)
        hash_digest = k.digest()

        # Эфирный Bloom фильтр использует 3 индекса
        indexes = []
        for i in range(0, 6, 2):
            v = (hash_digest[i] << 8) + hash_digest[i + 1]
            indexes.append(v % self.size)
        return indexes

    def add(self, data: bytes):
        for idx in self._get_indexes(data):
            self.bit_array |= (1 << idx)

    def check(self, data: bytes) -> bool:
        return all((self.bit_array >> idx) & 1 for idx in self._get_indexes(data))
