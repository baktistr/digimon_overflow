#!/bin/sh
cd /app
exec socat TCP-LISTEN:9999,reuseaddr,fork EXEC:"/app/digimon",pty,stderr,setsid,sane
