FROM docker.io/library/python:3.11.1-slim-bullseye

ENV \
    DEBCONF_NONINTERACTIVE_SEEN="true" \
    DEBIAN_FRONTEND="noninteractive" \
    APT_KEY_DONT_WARN_ON_DANGEROUS_USAGE="DontWarn"

WORKDIR /app

COPY . .

RUN \
    pip install --no-cache-dir -r requirements.txt \
    && \
    apt-get -qq update \
    && \
    apt-get install --no-install-recommends -y \
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

ENTRYPOINT ["/usr/bin/tini", "--", "/usr/local/bin/python3", "/app/intel-gpu-exporter.py"]

LABEL \
    org.opencontainers.image.title="intel-gpu-exporter" \
    org.opencontainers.image.authors="Devin Buhl <devin.kray@gmail.com>" \
    org.opencontainers.image.source="https://github.com/onedr0p/intel-gpu-exporter"
