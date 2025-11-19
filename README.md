# 🎮 Digimon Digital Adventure - CTF Challenge

A Capture The Flag (CTF) binary exploitation challenge featuring heap overflow exploitation with an interactive Digimon-themed interface.

## 📋 Overview

**Challenge Type:** Binary Exploitation (Pwn)
**Difficulty:** Medium
**Topic:** Heap Buffer Overflow, Function Pointer Hijacking
**Theme:** Digimon Digital World Adventure

Players must exploit a heap buffer overflow vulnerability to redirect program execution and unlock the legendary Omegamon, revealing the flag.

## 🎯 Challenge Features

### Interactive Gameplay
Unlike basic CTF challenges, this features a full interactive menu system:
- **Name your Digimon** - Set your partner's name (vulnerable input!)
- **Training system** - Increase stats and experience
- **Status viewer** - Check your Digimon's current state
- **Battle mode** - Trigger the function pointer (exploitation point)
- **Multiple functions** - Three different Digimon functions to discover

### Educational Value
This challenge teaches:
- ✅ Heap memory allocation and layout
- ✅ Buffer overflow exploitation beyond stack overflows
- ✅ Function pointer hijacking techniques
- ✅ Using GDB for dynamic analysis
- ✅ Calculating precise memory offsets
- ✅ Interactive exploitation with menu systems

## 🚀 Quick Start

### Prerequisites
```bash
# Required tools
- gcc
- make
- gdb (optional, for analysis)
- python3 (for solution script)
- docker (optional, for deployment)
```

### Setup
```bash
# 1. Clone or download the challenge files
cd digimon-challenge

# 2. Run the setup script
chmod +x setup-challenge.py
python3 setup-challenge.py

# 3. Test the challenge locally
./digimon
```

## 📁 Repository Structure

```
digimon-challenge/
├── digimon.c              # Source code (vulnerable program)
├── digimon                # Compiled binary (generated)
├── flag.txt               # Challenge flag (generated)
├── problem.md             # Challenge description for players
├── solution.py            # Detailed exploitation walkthrough
├── setup-challenge.py     # Environment setup script
├── Dockerfile             # Container deployment
├── Makefile              # Build configuration
└── README.md             # This file
```

## 🔧 Usage

### Local Testing
```bash
# Compile the binary
make

# Run the challenge
./digimon

# Try the interactive menu
# Option 1: Name your Digimon
# Option 4: Battle (triggers function pointer)
```

### Docker Deployment
```bash
# Build the container
docker build -t digimon-challenge .

# Run on port 9999
docker run -d -p 9999:9999 --name digimon digimon-challenge

# Test connection
nc localhost 9999
```

### Working on the Solution
```bash
# Interactive solution walkthrough
python3 solution.py

# Follow the menu:
# 1. Local exploitation (automatic)
# 2. Remote exploitation (specify host/port)
# 3. Manual exploitation steps (tutorial)
```

## 🎓 How It Works

### The Vulnerability

The program allocates two structures on the heap:

```c
struct DigimonData {
    char name[64];      // Vulnerable buffer
    int power_level;
    int experience;
};

struct BattleSystem {
    int (*battle_function)();  // Function pointer - our target!
    int evolution_stage;
    char digital_signature[16];
};
```

The vulnerability exists in the name input:
```c
strcpy(digimon->name, input);  // No bounds checking!
```

### Exploitation Strategy

1. **Overflow the name buffer** (64 bytes)
2. **Overflow through the struct padding** (8 bytes)
3. **Overwrite the function pointer** in the next heap chunk
4. **Trigger the function** by choosing the battle option
5. **Get redirected to omegamon_appears()** which prints the flag

### Memory Layout
```
[name buffer 64 bytes][power 4][exp 4][metadata][func_ptr 8][stage 4][sig 16]
                                                  ↑
                                                  TARGET
```

## 🛡️ Security Concepts Demonstrated

### Vulnerabilities
- **Heap Buffer Overflow** - Unsafe `strcpy()` without bounds checking
- **Function Pointer Hijacking** - Overwriting execution flow
- **No Input Validation** - Menu accepts arbitrary input length

### Mitigations NOT Present (Intentionally for Educational Purposes)
- ❌ No ASLR (Position Independent Executable disabled)
- ❌ No stack canaries (not needed for heap exploitation)
- ❌ No bounds checking on user input
- ❌ No modern heap protections

### Real-World Context
In production code, you would need:
- ✅ Input validation and sanitization
- ✅ Safe string functions (`strncpy`, `strlcpy`, or better yet, avoid C strings)
- ✅ ASLR and PIE enabled
- ✅ Heap protection mechanisms
- ✅ Address sanitizers during development

## 🔍 Debugging Tips

### Using GDB
```bash
# Start GDB
gdb ./digimon

# Set breakpoint at main
break main

# Run and step through
run
next

# Examine heap allocations
print digimon
print battle
print &battle->battle_function

# View memory
x/20gx digimon
x/20gx battle

# Find function address
print &omegamon_appears
```

### Finding Addresses
```bash
# Method 1: objdump
objdump -d digimon | grep omegamon_appears

# Method 2: nm
nm digimon | grep omegamon

# Method 3: readelf
readelf -s digimon | grep omegamon
```

## 🏆 Solution Hints

<details>
<summary>Hint 1: Understanding the Exploit (Click to expand)</summary>

The vulnerability is in the name input. When you enter your Digimon's name, the program uses `strcpy()` which doesn't check the length. This allows you to write beyond the allocated buffer.
</details>

<details>
<summary>Hint 2: What to Overwrite (Click to expand)</summary>

The goal is to overwrite the `battle_function` pointer in the `BattleSystem` structure. This pointer is called when you choose option 4 (Battle). If you can change it to point to `omegamon_appears`, you'll get the flag!
</details>

<details>
<summary>Hint 3: Calculating the Offset (Click to expand)</summary>

Use GDB to find the exact distance between the start of `digimon->name` and `battle->battle_function`. Typically this is 72 bytes (64 for name + 4 for power + 4 for exp), but verify with your system!
</details>

<details>
<summary>Hint 4: Crafting the Payload (Click to expand)</summary>

Your payload structure:
1. 72 bytes of padding (can be 'A's)
2. 8 bytes containing the address of `omegamon_appears` in little-endian format

Use Python: `payload = b"A"*72 + p64(address)`
</details>

## 📚 Learning Resources

- [Heap Exploitation Basics](https://heap-exploitation.dhavalkapil.com/)
- [LiveOverflow Heap Exploitation](https://www.youtube.com/playlist?list=PLhixgUqwRTjxglIswKp9mpkfPNfHkzyeN)
- [Pwntools Documentation](https://docs.pwntools.com/)
- [GDB Cheat Sheet](https://darkdust.net/files/GDB%20Cheat%20Sheet.pdf)

## 🎮 Playing the Challenge

### As a Player (CTF Participant)
You would receive:
- `digimon` binary
- Connection information
- `problem.md` description

You should NOT have access to:
- `digimon.c` source code
- `solution.py`
- `flag.txt`

### As an Organizer (CTF Host)
1. Run `setup-challenge.py` to generate flag and compile binary
2. Deploy using Docker or run directly with socat
3. Provide players with the binary and challenge description
4. Keep the solution and flag secure

## 🐛 Troubleshooting

### Compilation Issues
```bash
# If gcc is not found
sudo apt-get install build-essential  # Debian/Ubuntu
brew install gcc                       # macOS

# If you get permission errors
chmod +x setup-challenge.py
chmod +x digimon
```

### Exploitation Issues
```bash
# If offset is wrong, use GDB to find correct offset
gdb ./digimon
# (follow debugging tips above)

# If addresses are different, check if PIE is disabled
checksec digimon
# Should show: PIE: No PIE
```

### Docker Issues
```bash
# If port is already in use
docker stop digimon
docker rm digimon

# If build fails
docker build --no-cache -t digimon-challenge .
```

## 🤝 Contributing

This challenge is designed for educational purposes. Feel free to:
- Modify the difficulty
- Add more features
- Create variations
- Use in your CTF events

## ⚖️ License

This CTF challenge is released for educational purposes. Use responsibly and only in authorized environments.

## 👤 Author

Created as an educational binary exploitation challenge inspired by the Digimon series.

## 🎉 Credits

- Original inspiration: Pokemon Journey CTF by sspivey98
- Theme: Digimon franchise
- Educational purpose: Teaching heap exploitation concepts

---

**⚡ Good luck, DigiDestined! May you master the Digital World! ⚡**
