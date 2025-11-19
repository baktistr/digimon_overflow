FROM ubuntu:22.04

# Accept FLAG as build argument (CMGR will provide this)
ARG FLAG=picoCTF{test_flag_please_ignore}

# Install necessary packages
RUN apt-get update && apt-get install -y \
    gcc \
    make \
    gdb \
    socat \
    python3 \
    && rm -rf /var/lib/apt/lists/*

# Create challenge directory
RUN mkdir /challenge
WORKDIR /challenge

# Copy challenge files
COPY digimon.c /challenge/
COPY Makefile /challenge/
COPY setup-challenge.py /challenge/

# Run setup script to create flag and metadata
RUN FLAG="${FLAG}" python3 /challenge/setup-challenge.py

# Compile the binary
RUN make

# Create non-root user for the challenge
RUN useradd -m -s /bin/bash ctf

# Set proper permissions
RUN chown -R root:ctf /challenge && \
    chmod 750 /challenge && \
    chmod 640 /challenge/flag.txt && \
    chmod 755 /challenge/digimon

# Switch to ctf user
USER ctf

# Expose port for network service
EXPOSE 9999

# Start the challenge service
CMD ["socat", "TCP-LISTEN:9999,reuseaddr,fork", "EXEC:/challenge/digimon"]
