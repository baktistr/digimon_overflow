# Digimon Overflow

- Namespace: 18739
- ID: digimon-overflow
- Type: custom
- Category: Heap overflow
- Points: 40
- Templatable: no
- MaxUsers: 1

## Description

You've been selected as a DigiDestined - chosen to partner with a Digimon and save the Digital World! Your journey begins with a small Rookie-level Digimon named Agumon. You can train your digimon to be a powerful Champion-level digimon named Greymon, but legends speak of a powerful Mega-level Digimon named WarGreymon that holds incredible power.

However, there's a problem... The Digital World's digivolution system seems to have some... glitches.

Your mission: Train your Digimon, trigger the digivolution sequence, and exploit the glitches to unlock WarGreymon's true power and retrieve the sacred flag!

## Details

`$ nc {{server}} {{port}}`
The program's binary can be downloaded {{url_for("digimon", "here")}}.

## Hints

- *"The Digital World stores data in mysterious ways..."* - Think about heap memory allocation
- *"The first naming is safe, but digivolution changes everything..."* - Where is the vulnerability?
- *"A Digimon's new name during digivolution carries more power than you might think..."* - Buffer overflows can be powerful
- *"Evolution is all about transformation..."* - Function pointers can be overwritten
- *"Use your Digivice (debugger) to scan the Digital World!"* - GDB is your friend
- *"The structures are allocated on the heap, one after another..."* - Heap layout matters

## Solution Overview

1. **Reconnaissance**: Use `nm` or GDB to find `wargreymon_appears` address 
2. **Offset Calculation**: Determine distance to function pointer 
3. **Payload Crafting**:
   ```python
   import struct
   payload = b"A" * (some buffer size here)
   ```
4. **Exploitation**: Send payload during digivolution rename
5. **Flag Capture**: WarGreymon appears with flag!

## Challenge Options

## Learning Objective

This challenge demonstrates:
- **Secure vs Insecure**: `strncpy()` (safe) vs `strcpy()` (unsafe)
- **Heap Exploitation**: Beyond traditional stack-based overflows
- **Control Flow Hijacking**: Function pointer redirection
- **Null Byte Handling**: Partial pointer overwrite with `strcpy()`
- **Realistic CTF Design**: Progressive difficulty with gameplay elements

## Attributes

- author: baktistr