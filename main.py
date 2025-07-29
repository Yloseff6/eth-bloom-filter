from bloom_filter import BloomFilter


def address_to_bytes(address: str) -> bytes:
    address = address.lower().replace("0x", "")
    return bytes.fromhex(address)


if __name__ == "__main__":
    bloom = BloomFilter()

    addr1 = "0x6Fb2c634a3360f4e9cdeB47DdDD2A269A26f5B7a"
    addr2 = "0x1111111111111111111111111111111111111111"

    addr1_bytes = address_to_bytes(addr1)
    addr2_bytes = address_to_bytes(addr2)

    bloom.add(addr1_bytes)

    print(f"{addr1} in bloom? {bloom.check(addr1_bytes)}")
    print(f"{addr2} in bloom? {bloom.check(addr2_bytes)}")
