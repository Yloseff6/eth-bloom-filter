import argparse
from bloom_filter import BloomFilter


def address_to_bytes(address: str) -> bytes:
    address = address.lower()
    if address.startswith("0x"):
        address = address[2:]
    if len(address) != 40:
        raise ValueError(f"Invalid Ethereum address: {address}")
    return bytes.fromhex(address)


def print_result(address: str, result: bool):
    status = "✅ FOUND" if result else "❌ NOT FOUND"
    print(f"{address} → {status}")


def main():
    parser = argparse.ArgumentParser(description="Ethereum Bloom Filter Tool")
    parser.add_argument(
        "--add", nargs="+", help="Ethereum address(es) to add to the bloom filter"
    )
    parser.add_argument(
        "--check", nargs="+", help="Ethereum address(es) to check in the bloom filter"
    )
    args = parser.parse_args()

    bloom = BloomFilter()

    if args.add:
        for addr in args.add:
            try:
                bloom.add(address_to_bytes(addr))
                print(f"Added: {addr}")
            except ValueError as e:
                print(e)

    if args.check:
        for addr in args.check:
            try:
                result = bloom.check(address_to_bytes(addr))
                print_result(addr, result)
            except ValueError as e:
                print(e)

    if not args.add and not args.check:
        parser.print_help()


if __name__ == "__main__":
    main()
