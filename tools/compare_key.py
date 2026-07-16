#!/usr/bin/env python3

import time

PREAMBLE = "10101001"
EOM      = "11111111"

def file_to_bits(path):
    with open(path, "rb") as f:
        data = f.read()
    return "".join(f"{byte:08b}" for byte in data)

def find_framed_payload(bits):
    start = bits.find(PREAMBLE)
    if start == -1:
        raise RuntimeError("Preamble not found")

    start += len(PREAMBLE)
    end = bits.find(EOM, start)
    if end == -1:
        raise RuntimeError("End-of-message not found")

    return bits[start:end]

def compare_bits(rx_bits, key_bits):
    mismatches = []
    min_len = min(len(rx_bits), len(key_bits))

    for i in range(min_len):
        if rx_bits[i] != key_bits[i]:
            mismatches.append(i)

    return mismatches, min_len

def main():
    import argparse

    parser = argparse.ArgumentParser(description="Compare a received RAMBO bitstream against a reference key/file")
    parser.add_argument("--received", default="/tmp/output.bin", help="Received bitstream file produced by the GNU Radio flowgraph")
    parser.add_argument("--key", default="data/aes.key", help="Reference key or payload file to compare against")
    args = parser.parse_args()

    rx_bits  = file_to_bits(args.received)
    key_bits = file_to_bits(args.key)

    payload_bits = find_framed_payload(rx_bits)

    mismatches, compared = compare_bits(payload_bits, key_bits)

    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}]")
    print("Original:")
    print(key_bits[:compared])
    print()
    print("Received:")
    print(payload_bits[:compared])
    print()

    print(f"Key length:      {len(key_bits)} bits")
    print(f"Received length: {len(payload_bits)} bits")
    print(f"Compared:        {compared} bits")
    print()

    if not mismatches:
        print("✓ Perfect match — no bit errors detected")
    else:
        print(f"✗ {len(mismatches)} bit errors detected")
        print("First 16 mismatches at bit positions:")
        for i in mismatches[:16]:
            print(f"  bit {i}: rx={payload_bits[i]} key={key_bits[i]}")

if __name__ == "__main__":
    main()
