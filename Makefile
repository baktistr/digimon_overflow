# Makefile for Digimon Overflow CTF Challenge

# Compiler settings
CC = gcc
CFLAGS = -fno-stack-protector -no-pie -w
TARGET = digimon
SOURCE = digimon.c
FLAG_FILE = flag.txt

# Default target
all: $(TARGET)

# Compile the binary
$(TARGET): $(SOURCE)
	@echo "[*] Compiling $(TARGET)..."
	$(CC) $(CFLAGS) -o $(TARGET) $(SOURCE)
	@chmod 755 $(TARGET)
	@echo "[+] Compilation successful!"
	@echo "[+] Binary: $(TARGET)"

# Create a test flag if it doesn't exist
flag:
	@if [ ! -f $(FLAG_FILE) ]; then \
		echo "flag{test_flag_replace_with_real_flag}" > $(FLAG_FILE); \
		chmod 640 $(FLAG_FILE); \
		echo "[+] Test flag created: $(FLAG_FILE)"; \
	else \
		echo "[*] Flag file already exists: $(FLAG_FILE)"; \
	fi

# Full setup (compile + flag)
setup: flag $(TARGET)
	@echo "[+] Setup complete!"

# Clean compiled files
clean:
	@echo "[*] Cleaning up..."
	@rm -f $(TARGET)
	@rm -f *.o
	@echo "[+] Cleanup complete!"

# Clean everything including flag
cleanall: clean
	@rm -f $(FLAG_FILE)
	@echo "[+] All files cleaned!"

# Run the challenge locally
run: $(TARGET)
	@echo "[*] Starting challenge..."
	@./$(TARGET)

# Debug mode with GDB
debug: $(TARGET)
	@echo "[*] Starting GDB..."
	@gdb ./$(TARGET)

# Check binary security features
check: $(TARGET)
	@echo "[*] Checking binary security features..."
	@if command -v checksec > /dev/null 2>&1; then \
		checksec --file=$(TARGET); \
	else \
		echo "[!] checksec not found. Install pwntools or checksec.sh"; \
		echo "[*] Manual check:"; \
		readelf -h $(TARGET) | grep -E "Type|Entry"; \
	fi

# Disassemble the binary
disasm: $(TARGET)
	@echo "[*] Disassembling $(TARGET)..."
	@objdump -d $(TARGET) | less

# Show symbols
symbols: $(TARGET)
	@echo "[*] Showing symbols in $(TARGET)..."
	@nm $(TARGET) | grep -E "(agumon|greymon|wargreymon|main)"

# Docker targets
docker-build:
	@echo "[*] Building Docker image..."
	@docker build -t digimon-challenge .
	@echo "[+] Docker image built: digimon-challenge"

docker-run:
	@echo "[*] Running Docker container..."
	@docker run -d -p 9999:9999 --name digimon digimon-challenge
	@echo "[+] Container running on port 9999"
	@echo "[*] Connect with: nc localhost 9999"

docker-stop:
	@echo "[*] Stopping Docker container..."
	@docker stop digimon
	@docker rm digimon
	@echo "[+] Container stopped and removed"

docker-logs:
	@docker logs -f digimon

# Test with a simple payload
test: $(TARGET)
	@echo "[*] Testing with simple input..."
	@echo "AAAA" | ./$(TARGET)

# Show file info
info: $(TARGET)
	@echo "[*] File information:"
	@file $(TARGET)
	@echo ""
	@echo "[*] File size:"
	@ls -lh $(TARGET)
	@echo ""
	@echo "[*] Strings containing 'flag':"
	@strings $(TARGET) | grep -i flag || echo "No flag strings found"

# Help menu
help:
	@echo "Digimon Overflow - CTF Challenge Makefile"
	@echo ""
	@echo "Available targets:"
	@echo "  make              - Compile the binary (default)"
	@echo "  make all          - Same as default"
	@echo "  make setup        - Full setup (compile + create flag)"
	@echo "  make flag         - Create test flag file"
	@echo "  make clean        - Remove compiled binary"
	@echo "  make cleanall     - Remove binary and flag"
	@echo "  make run          - Run the challenge locally"
	@echo "  make debug        - Start GDB debugger"
	@echo "  make check        - Check binary security features"
	@echo "  make disasm       - Disassemble the binary"
	@echo "  make symbols      - Show important symbols"
	@echo "  make test         - Test with simple input"
	@echo "  make info         - Show binary information"
	@echo "  make docker-build - Build Docker image"
	@echo "  make docker-run   - Run Docker container"
	@echo "  make docker-stop  - Stop Docker container"
	@echo "  make docker-logs  - View Docker logs"
	@echo "  make help         - Show this help message"
	@echo ""
	@echo "Example workflow:"
	@echo "  make setup        # Initial setup"
	@echo "  make debug        # Analyze with GDB"
	@echo "  make docker-build # Build container"
	@echo "  make docker-run   # Deploy challenge"

.PHONY: all setup flag clean cleanall run debug check disasm symbols docker-build docker-run docker-stop docker-logs test info help
