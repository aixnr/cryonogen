FROM python:3.11-slim-bookworm
ARG S6_OVERLAY_VERSION=3.2.0.0

RUN apt-get update && apt-get --assume-yes --no-install-recommends install curl xz-utils \
    && curl -SLO https://github.com/just-containers/s6-overlay/releases/download/v${S6_OVERLAY_VERSION}/s6-overlay-noarch.tar.xz \
    && curl -SLO https://github.com/just-containers/s6-overlay/releases/download/v${S6_OVERLAY_VERSION}/s6-overlay-x86_64.tar.xz \
    && tar -C / -Jxpf s6-overlay-noarch.tar.xz \
    && tar -C / -Jxpf s6-overlay-x86_64.tar.xz \
    && rm -rf s6-overlay-noarch.tar.xz s6-overlay-x86_64.tar.xz \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && curl -SLO "https://github.com/astral-sh/uv/releases/download/0.5.1/uv-x86_64-unknown-linux-gnu.tar.gz" \
    && tar axf uv-x86_64-unknown-linux-gnu.tar.gz \
    && mv uv-x86_64-unknown-linux-gnu/uv /usr/local/bin/uv \
    && rm -rf uv-x86_64-unknown-linux-gnu uv-x86_64-unknown-linux-gnu.tar.gz \
    && uv python install 3.11 \
    && uv venv shard && . /shard/bin/activate \
    && uv pip install pandas Flask Flask-Cors

COPY ./cryosrc /cryosrc
COPY pyproject.toml /pyproject.toml

RUN . /shard/bin/activate \
    && cd / && uv pip install . \
    && ln -s /shard/bin/cryo /usr/local/bin/cryo \
    && echo "#!/bin/bash\ncd / && cryo web --port 5000 --host 0.0.0.0 --db /datasheet/cryonogen.db" >> cryo.sh \
    && chmod +x cryo.sh

COPY ./bin/cryoserve /usr/local/bin/cryoserve

RUN mkdir -p /etc/services.d/cryo_be \
    && mkdir -p /etc/services.d/cryo_fe \
    && echo "#!/command/execlineb -P\nbash /cryo.sh" >> /etc/services.d/cryo_be/run \
    && echo "#!/command/execlineb -P\ncryoserve -port 9091" >> /etc/services.d/cryo_fe/run \
    && chmod +x /etc/services.d/cryo_be/run \
    && chmod +x /etc/services.d/cryo_fe/run

ENTRYPOINT ["/init"]
