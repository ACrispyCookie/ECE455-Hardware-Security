def extract_message(filename,
                    preamble="10101001",
                    eom="11111111"):
    # Read file as raw bytes
    with open(filename, "rb") as f:
        data = f.read()

    # Convert bytes to a continuous bit string
    bitstream = "".join(f"{byte:08b}" for byte in data)

    # Find preamble
    start = bitstream.find(preamble)
    if start == -1:
        raise ValueError("Preamble not found")

    # Start reading right after preamble
    cursor = start + len(preamble)
    message_bits = ""

    while cursor + 8 <= len(bitstream):
        byte = bitstream[cursor:cursor + 8]

        if byte == eom:
            break

        message_bits += byte
        cursor += 8

    # Convert message bits to characters
    message = ""
    for i in range(0, len(message_bits), 8):
        byte = message_bits[i:i + 8]
        message += chr(int(byte, 2))

    return message


if __name__ == "__main__":
    filename = "/home/tsiantosd/Desktop/output.txt"
    msg = extract_message(filename)
    print("Decoded message:")
    print(msg)
