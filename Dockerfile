FROM docker.io/library/python:3.9.13

ENV \
    DEBCONF_NONINTERACTIVE_SEEN=true \
    DEBIAN_FRONTEND="noninteractive" \
    APT_KEY_DONT_WARN_ON_DANGEROUS_USAGE=DontWarn

WORKDIR /app

COPY . .

RUN \
    pip install -r requirements.txt \
    && \
    apt-get -qq update \
    && \
    apt-get install -y \
        intel-gpu-tools \
        tini \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && apt-get autoremove -y \
    && apt-get clean \
    && \
    rm -rf \
        /tmp/* \
        /var/lib/apt/lists/* \
        /var/cache/apt/* \
        /var/tmp/*

COPY intel-gpu-exporter.py .
ENTRYPOINT ["/usr/bin/tini", "--", "/usr/local/bin/python3", "/app/intel-gpu-exporter.py"]

EXPOSE 8080/tcp

LABEL \
    org.opencontainers.image.base.name="ghcr.io/onedr0p/intel-gpu-exporter" \
    org.opencontainers.image.authors="Devin Buhl <devin.kray@gmail.com>"
