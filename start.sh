#!/bin/bash
# Start script for Digimon Digital Adventure CTF Challenge
# This script launches the challenge service using socat

PORT=${PORT:-9999}
BINARY="./digimon"

echo "=================================="
echo "Digimon Digital Adventure"
echo "CTF Challenge Service"
echo "=================================="
echo "Starting service on port $PORT..."
echo ""

if [ ! -f "$BINARY" ]; then
    echo "Error: Binary '$BINARY' not found!"
    echo "Please run 'make' or 'python3 setup-challenge.py' first."
    exit 1
fi

if [ ! -f "flag.txt" ]; then
    echo "Warning: flag.txt not found!"
    echo "Creating a test flag..."
    echo "flag{test_flag_run_setup_script}" > flag.txt
    chmod 640 flag.txt
fi

echo "Service starting..."
echo "Connect with: nc localhost $PORT"
echo ""
echo "Press Ctrl+C to stop the service"
echo "=================================="
echo ""

# Start the service
socat TCP-LISTEN:$PORT,reuseaddr,fork EXEC:$BINARY
