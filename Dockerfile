FROM debian:bookworm-slim AS base

RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y \
    python3 \
    gcc \
    socat \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir /challenge && chmod 700 /challenge

COPY digimon.c setup-challenge.py /app/
COPY start.sh /opt/
RUN chmod +x /opt/start.sh

WORKDIR /app/
RUN gcc -O0 -fno-stack-protector -no-pie -w digimon.c -o digimon
RUN tar czvf /challenge/artifacts.tar.gz digimon

FROM base AS challenge
ARG FLAG=picoCTF{test_flag_please_ignore}

RUN FLAG="${FLAG}" python3 /app/setup-challenge.py

EXPOSE 9999
# PUBLISH 9999 AS socat

CMD ["/opt/start.sh"]
