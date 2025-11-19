#!/usr/bin/env python3
"""
Digimon Digital Adventure - CTF Challenge Setup Script
This script initializes the challenge environment and generates the flag.
"""

import os
import sys
import subprocess
import random
import string

def generate_flag():
    """Generate a random flag for the challenge"""
    adjectives = ["legendary", "ultimate", "mega", "digital", "ancient", "mystic", "supreme"]
    nouns = ["warrior", "guardian", "champion", "master", "hero", "destined", "evolved"]

    adj = random.choice(adjectives)
    noun = random.choice(nouns)
    random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=12))

    flag = f"flag{{{adj}_{noun}_{random_str}}}"
    return flag

def create_flag_file():
    """Create flag.txt with a random flag"""
    flag = generate_flag()

    with open("flag.txt", "w") as f:
        f.write(flag + "\n")

    print(f"[+] Flag generated: {flag}")
    print(f"[+] Flag saved to flag.txt")

    # Set restrictive permissions
    os.chmod("flag.txt", 0o640)
    print(f"[+] Permissions set to 640")

    return flag

def compile_binary():
    """Compile the digimon binary"""
    print("\n[*] Compiling digimon binary...")

    if not os.path.exists("digimon.c"):
        print("[!] Error: digimon.c not found!")
        return False

    try:
        # Compile with appropriate flags
        # -fno-stack-protector: Disable stack canaries
        # -z execstack: Make stack executable (not needed for heap)
        # -no-pie: Disable Position Independent Executable
        result = subprocess.run(
            ["gcc", "-o", "digimon", "digimon.c",
             "-fno-stack-protector", "-no-pie", "-w"],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            print("[+] Binary compiled successfully!")
            os.chmod("digimon", 0o755)
            return True
        else:
            print(f"[!] Compilation failed: {result.stderr}")
            return False

    except FileNotFoundError:
        print("[!] Error: gcc not found. Please install gcc.")
        return False

def verify_setup():
    """Verify all required files are present"""
    print("\n[*] Verifying setup...")

    required_files = ["digimon.c", "digimon", "flag.txt", "Dockerfile", "problem.md"]
    missing = []

    for file in required_files:
        if os.path.exists(file):
            print(f"[+] Found: {file}")
        else:
            print(f"[!] Missing: {file}")
            missing.append(file)

    if missing:
        print(f"\n[!] Warning: Missing files: {', '.join(missing)}")
        return False

    print("\n[+] All required files present!")
    return True

def display_instructions():
    """Display setup completion instructions"""
    print("\n" + "="*60)
    print("🎮 DIGIMON DIGITAL ADVENTURE - CTF CHALLENGE SETUP COMPLETE 🎮")
    print("="*60)
    print("\nNext steps:")
    print("\n1. Test the challenge locally:")
    print("   $ ./digimon")
    print("\n2. Build Docker container:")
    print("   $ docker build -t digimon-challenge .")
    print("\n3. Run Docker container:")
    print("   $ docker run -d -p 9999:9999 --name digimon digimon-challenge")
    print("\n4. Test remote connection:")
    print("   $ nc localhost 9999")
    print("\n5. View the challenge description:")
    print("   $ cat problem.md")
    print("\n6. Work on the solution:")
    print("   $ python3 solution.py")
    print("\n" + "="*60)

def main():
    """Main setup function"""
    print("""
    ╔═══════════════════════════════════════════════════════╗
    ║   DIGIMON DIGITAL ADVENTURE - CTF SETUP SCRIPT        ║
    ║   Setting up your challenge environment...            ║
    ╚═══════════════════════════════════════════════════════╝
    """)

    # Create flag
    create_flag_file()

    # Compile binary
    if not compile_binary():
        print("\n[!] Setup incomplete due to compilation error.")
        sys.exit(1)

    # Verify everything is set up
    if not verify_setup():
        print("\n[!] Setup incomplete due to missing files.")
        sys.exit(1)

    # Show instructions
    display_instructions()

    print("\n✅ Setup completed successfully!")
    print("🚀 Your CTF challenge is ready to deploy!\n")

if __name__ == "__main__":
    main()
