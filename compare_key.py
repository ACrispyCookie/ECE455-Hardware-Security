#!/usr/bin/env python3

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
    rx_bits  = file_to_bits("/tmp/output.bin")
    key_bits = file_to_bits("./aes.key")

    payload_bits = find_framed_payload(rx_bits)

    mismatches, compared = compare_bits(payload_bits, key_bits)

    print(f"Key length:      {len(key_bits)} bits")
    print(f"Received length: {len(payload_bits)} bits")
    print(f"Compared:        {compared} bits")

    if not mismatches:
        print("✓ Perfect match — no bit errors detected")
    else:
        print(f"✗ {len(mismatches)} bit errors detected")
        print("First 16 mismatches at bit positions:")
        for i in mismatches[:16]:
            print(f"  bit {i}: rx={payload_bits[i]} key={key_bits[i]}")

if __name__ == "__main__":
    main()
