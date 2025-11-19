# Digimon Overflow - CTF Challenge

## Challenge Information
- **Name:** Digimon Overflow
- **Category:** Binary Exploitation / Pwn
- **Difficulty:** Medium
- **Points:** 400

## Story

You've been selected as a DigiDestined - chosen to partner with a Digimon and save the Digital World! Your journey begins with a small Rookie-level Digimon named **Agumon**. You can train your digimon to be a powerful Champion-level digimon named **Greymon**, but legends speak of a powerful Mega-level Digimon named **WarGreymon** that holds incredible power.

However, there's a problem... The Digital World's digivolution system seems to have some... *glitches*.

Your mission: Train your Digimon, trigger the digivolution sequence, and exploit the glitches to unlock WarGreymon's true power and retrieve the sacred flag!

## Challenge Description

You're given access to a Digimon training simulator with an interactive menu system. The program allows you to:
- Name your Digimon (initially safe)
- Train to increase stats
- View current stats
- Challenge opponents (coming soon)
- Exit the program
- Digivolve (unlocks at 50 experience)

The challenge flow:
1. **Initial Setup**: Name your Digimon safely (no overflow here)
2. **Training Phase**: Train your Digimon to gain experience (need 50 exp to unlock digivolve)
3. **Digivolution**: When ready, digivolution forces you to rename your Digimon...
4. **Exploit**: During the digivolution rename, there's a vulnerability!

Somewhere in the Digital World's digivolution code lies a heap overflow vulnerability. Can you manipulate the heap memory to trigger the legendary WarGreymon and claim your flag?

## Objectives

1. Train your Digimon to reach 50 experience points
2. Trigger the digivolution sequence
3. Analyze the heap layout during digivolution
4. Identify the heap overflow vulnerability during rename
5. Craft an exploit to overwrite the function pointer
6. Trigger the `wargreymon_appears()` function to retrieve the flag

## Hints

- *"The Digital World stores data in mysterious ways..."* - Think about heap memory allocation
- *"The first naming is safe, but digivolution changes everything..."* - Where is the vulnerability?
- *"A Digimon's new name during digivolution carries more power than you might think..."* - Buffer overflows can be powerful
- *"Evolution is all about transformation..."* - Function pointers can be overwritten
- *"Use your Digivice (debugger) to scan the Digital World!"* - GDB is your friend
- *"The structures are allocated on the heap, one after another..."* - Heap layout matters

## Learning Objectives

This challenge teaches:
- Heap memory layout and allocation
- Buffer overflow exploitation on the heap
- Function pointer hijacking
- Using GDB for memory analysis
- Calculating offsets for precise overwrites

## Files Provided
- `digimon` - The compiled binary
- `digimon.c` - Source code (for educational purposes)

## Connection Info
- Local: `./digimon`
- Remote: `nc <server-ip> 9999`

## Flag Format
`picoCTF{...}`

---

*Good luck, DigiDestined! The fate of the Digital World is in your hands!* ⚡
