# Digimon Digital Adventure - CTF Challenge

## Challenge Information
- **Name:** Digimon Digital Adventure
- **Category:** Binary Exploitation / Pwn
- **Difficulty:** Medium
- **Points:** 350

## Story

You've been selected as a DigiDestined - chosen to partner with a Digimon and save the Digital World! Your journey begins with a small Rookie-level Digimon, but legends speak of a powerful Ultimate-level Digimon named **Omegamon** that holds incredible power.

However, there's a problem... The Digital World's training system seems to have some... *glitches*.

Your mission: Exploit these glitches to unlock Omegamon's true power and retrieve the sacred flag!

## Challenge Description

You're given access to a Digimon training simulator with an interactive menu system. The program allows you to:
- Name your Digimon
- Train to increase stats
- View current stats
- Battle opponents
- Exit the program

Somewhere in the Digital World's code lies a vulnerability. Can you manipulate the heap memory to trigger the legendary Omegamon and claim your flag?

## Objectives

1. Analyze the binary to understand the heap layout
2. Identify the vulnerability in the program
3. Craft an exploit to redirect program execution
4. Trigger the `omegamon_appears()` function to retrieve the flag

## Hints

- *"The Digital World stores data in mysterious ways..."* - Think about how memory is allocated
- *"A Digimon's name carries more power than you might think..."* - Buffer overflows can be powerful
- *"Evolution is all about transformation..."* - Function pointers can be overwritten
- *"Use your Digivice (debugger) to scan the Digital World!"* - GDB is your friend

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
`flag{...}`

---

*Good luck, DigiDestined! The fate of the Digital World is in your hands!* ⚡
