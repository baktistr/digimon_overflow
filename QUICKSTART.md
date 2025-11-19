# 🚀 Quick Start Guide

Get your Digimon CTF challenge running in 5 minutes!

## For Challenge Organizers

### Option 1: Quick Local Setup (30 seconds)
```bash
# Run the setup script
python3 setup-challenge.py

# Test it works
./digimon
```

### Option 2: Docker Deployment (2 minutes)
```bash
# Setup and build
python3 setup-challenge.py
docker build -t digimon-challenge .

# Run on port 9999
docker run -d -p 9999:9999 --name digimon digimon-challenge

# Test connection
nc localhost 9999
```

### Option 3: Using Makefile
```bash
# One command setup
make setup

# Run locally
make run

# Or deploy with Docker
make docker-build
make docker-run
```

## For CTF Participants

### Connect to Challenge
```bash
nc <challenge-server> <port>

# Example:
nc ctf.example.com 9999
```

### Recommended Tools
```bash
# Install pwntools (Python exploitation framework)
pip3 install pwntools

# GDB for debugging (already installed on most systems)
gdb --version

# Optional: GDB enhancements
sudo apt-get install gdb-peda  # Ubuntu/Debian
```

### First Steps
1. **Explore the program**
   - Run it locally if provided
   - Try all menu options
   - Look for suspicious inputs

2. **Analyze the binary**
   ```bash
   file digimon
   strings digimon | grep flag
   objdump -d digimon | grep omegamon
   ```

3. **Debug with GDB**
   ```bash
   gdb ./digimon
   (gdb) break main
   (gdb) run
   (gdb) info functions
   ```

4. **Find the vulnerability**
   - Which input accepts user data?
   - Is there bounds checking?
   - What happens with long input?

5. **Craft your exploit**
   - Calculate offset to function pointer
   - Find address of target function
   - Build payload: padding + address

## Need Help?

- 📖 Read [README.md](README.md) for full documentation
- 🎯 Read [problem.md](problem.md) for challenge description
- 💡 Check [solution.py](solution.py) for hints (organizers only!)
- 🐛 Debug with: `make debug`
- ℹ️  Binary info: `make info`

## Common Issues

### "Permission denied" when running
```bash
chmod +x digimon
./digimon
```

### "gcc: command not found"
```bash
# Ubuntu/Debian
sudo apt-get install build-essential

# macOS
xcode-select --install
```

### "docker: command not found"
```bash
# Install Docker from: https://docs.docker.com/get-docker/
```

### Binary crashes immediately
- Check if flag.txt exists
- Run: `make setup` to regenerate

## Exploitation Workflow

```
1. Reconnaissance
   └─> Understand what the program does

2. Analysis
   └─> Find the vulnerability (hint: naming your Digimon)

3. Discovery
   └─> Locate target function (hint: check for "omegamon")

4. Calculation
   └─> Determine offset to function pointer

5. Exploitation
   └─> Craft payload and trigger it

6. Victory
   └─> Capture the flag! 🏴
```

## Quick Commands Reference

```bash
# Setup
make setup              # Compile and create flag
make clean             # Clean up binaries
make cleanall          # Remove everything

# Testing
make run               # Run locally
make test              # Simple test
make debug             # Debug with GDB

# Analysis
make check             # Check security features
make disasm            # Disassemble binary
make symbols           # Show function symbols
make info              # Binary information

# Docker
make docker-build      # Build container
make docker-run        # Run container
make docker-stop       # Stop container
make docker-logs       # View logs
```

---

⚡ **Remember:** This challenge is for educational purposes. Use responsibly! ⚡
