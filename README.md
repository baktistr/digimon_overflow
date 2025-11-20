# Digimon Overflow

Heap exploitation CTF challenge featuring a heap overflow that lets players hijack a function pointer during digivolution.

## Files
- Dockerfile — container build (port 9999, uses `start.sh`).
- start.sh — runs `digimon` via socat on port 9999.
- digimon.c — challenge source; compiled to `digimon`.
- setup-challenge.py — writes flag/metadata inside the container.
- assets/ — ASCII art for the game.
- solver/solve.py — reference exploit for testing.
- flag.txt — placeholder flag for local runs.

## Build and Run
```bash
# Build with a custom flag
docker build --build-arg FLAG="picoCTF{test_flag}" -t digimon-overflow .

# Run on port 9999
docker run -d -p 9999:9999 --name digimon digimon-overflow

# Connect
nc localhost 9999
```

## Exploit Notes
1. Train until digivolution is available, then rename.
2. Rename uses `strcpy` into a 64-byte buffer; overflow the next heap chunk containing a function pointer.
3. Offset to `battle_function` is 96 bytes from `name[0]`; target `wargreymon_appears`.

## Troubleshooting
- Rebuild cleanly: `docker build --no-cache -t digimon-overflow .`
- Verify flag inside container: `docker run --rm digimon-overflow cat /challenge/flag.txt`

## CMGR Notes
- Build arg `FLAG` required; `setup-challenge.py` writes `/challenge/flag.txt` and `/challenge/metadata.json`.
- Publishes `digimon` as the only artifact (`/challenge/artifacts.tar.gz`).
- Listens on port 9999 via `start.sh` (socat to `/app/digimon`).
- No Makefile use in container; direct `gcc -O0 -fno-stack-protector -no-pie -w digimon.c -o digimon`.
