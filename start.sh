#!/bin/sh
cd /app
# Use stdbuf to disable buffering
exec socat TCP-LISTEN:9999,reuseaddr,fork EXEC:"stdbuf -i0 -o0 -e0 /app/digimon"
