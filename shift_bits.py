#!/usr/bin/env python3
import argparse

def shift_file_bits(input_path, output_path, shift_bits, direction):
    with open(input_path, "rb") as f:
        data = f.read()

    if not data:
        raise ValueError("Input file is empty")

    bit_len = len(data) * 8
    value = int.from_bytes(data, byteorder="big")

    if direction == "left":
        value = (value << shift_bits) & ((1 << bit_len) - 1)
    else:  # right
        value >>= shift_bits

    shifted = value.to_bytes(len(data), byteorder="big")

    with open(output_path, "wb") as f:
        f.write(shifted)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Bit-shift an entire file as a continuous bitstream")
    parser.add_argument("input", help="Input file")
    parser.add_argument("output", help="Output file")
    parser.add_argument("bits", type=int, help="Number of bits to shift")
    parser.add_argument("--direction", choices=["left", "right"], default="left",
                        help="Shift direction (default: left)")

    args = parser.parse_args()

    shift_file_bits(args.input, args.output, args.bits, args.direction)
