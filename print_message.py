import time
import sys

PREAMBLE = "10101001"
EOM = "11111111"

def stream_decode(filename):
    bit_buffer = ""
    message_started = False

    with open(filename, "rb") as f:
        f.seek(0, 0)

        while True:
            chunk = f.read(1024)
            if not chunk:
                time.sleep(0.05)
                continue

            for byte in chunk:
                bit_buffer += f"{byte:08b}"

                # Look for preamble only once
                if not message_started:
                    idx = bit_buffer.find(PREAMBLE)
                    if idx != -1:
                        bit_buffer = bit_buffer[idx + len(PREAMBLE):]
                        message_started = True
                    else:
                        # Keep buffer bounded
                        bit_buffer = bit_buffer[-len(PREAMBLE):]
                        continue

                # Decode full bytes
                while len(bit_buffer) >= 8:
                    b = bit_buffer[:8]
                    bit_buffer = bit_buffer[8:]

                    if b == EOM:
                        print("\n<EOM>")
                        return

                    sys.stdout.write(chr(int(b, 2)))
                    sys.stdout.flush()


if __name__ == "__main__":
    filename = sys.argv[1] if len(sys.argv) == 2 else "/tmp/output.bin"
    print("Listening for message...\n")
    stream_decode(filename)
