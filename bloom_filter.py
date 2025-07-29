from Crypto.Hash import keccak
from typing import List


class BloomFilter:
    def __init__(self, size: int = 2048) -> None:
        """
        Initializes a Bloom filter.

        Args:
            size (int): Number of bits in the filter. Ethereum uses 2048 by default.
        """
        self.size = size
        self.bit_array = 0  # Represented as an integer (bitfield)

    def _keccak256(self, data: bytes) -> bytes:
        """
        Returns keccak256 hash of the input data.

        Args:
            data (bytes): Data to hash.

        Returns:
            bytes: 32-byte keccak256 hash.
        """
        k = keccak.new(digest_bits=256)
        k.update(data)
        return k.digest()

    def _get_bit_indexes(self, data: bytes) -> List[int]:
        """
        Calculates 3 index positions using the first 6 bytes of keccak256 hash.

        Ethereum's log bloom uses only 3 bits per entry.

        Args:
            data (bytes): Data to hash and map to bits.

        Returns:
            List[int]: List of 3 bit indexes in the Bloom filter.
        """
        hashed = self._keccak256(data)
        indexes = []
        for i in range(0, 6, 2):  # 0-1, 2-3, 4-5
            value = (hashed[i] << 8) | hashed[i + 1]
            indexes.append(value % self.size)
        return indexes

    def add(self, data: bytes) -> None:
        """
        Adds an item to the Bloom filter.

        Args:
            data (bytes): Data to insert.
        """
        for index in self._get_bit_indexes(data):
            self.bit_array |= 1 << index

    def check(self, data: bytes) -> bool:
        """
        Checks if the item is possibly in the Bloom filter.

        Args:
            data (bytes): Data to check.

        Returns:
            bool: True if possibly present, False if definitely not present.
        """
        return all((self.bit_array >> index) & 1 for index in self._get_bit_indexes(data))

    def __repr__(self) -> str:
        return f"<BloomFilter size={self.size} bits_set={bin(self.bit_array).count('1')}>"
