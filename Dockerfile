# ------------------------------------------------------------------------------
# Builder
FROM debian:12 AS build_python

RUN apt-get update \
  && apt-get install --assume-yes --quiet --no-install-recommends \
  python3-minimal python3-venv python3-distutils \
  apt-transport-https ca-certificates \
  && update-ca-certificates

COPY ./cryo /src/cryo/
COPY Pipfile pyproject.toml src/
RUN echo "Zipping cryo with shiv" && cd /src \
  && python3 -m venv venv && . ./venv/bin/activate \
  && pip install pipenv && pipenv install \
  && shiv -c cryo -o /usr/local/bin/cryo --compressed .

FROM golang:1.21.5-bookworm AS build_go
COPY ./frontend /src/frontend/
COPY ./cryoserve.go /src/cryoserve.go
RUN echo "Compiling the frontend static assets" && cd /src \
  && go build -ldflags '-s -w' -o /usr/local/bin/cryoserve cryoserve.go


# ------------------------------------------------------------------------------
# Final
FROM python:3.11-slim-bookworm
ARG S6_OVERLAY_VERSION=3.2.0.0

RUN apt-get update && apt-get --assume-yes --no-install-recommends install curl xz-utils \
    && curl -SLO https://github.com/just-containers/s6-overlay/releases/download/v${S6_OVERLAY_VERSION}/s6-overlay-noarch.tar.xz \
    && curl -SLO https://github.com/just-containers/s6-overlay/releases/download/v${S6_OVERLAY_VERSION}/s6-overlay-x86_64.tar.xz \
    && tar -C / -Jxpf s6-overlay-noarch.tar.xz \
    && tar -C / -Jxpf s6-overlay-x86_64.tar.xz \
    && rm -rf s6-overlay-noarch.tar.xz s6-overlay-x86_64.tar.xz \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY --from=build_python /usr/local/bin/cryo /usr/local/bin/cryo
COPY --from=build_go /usr/local/bin/cryoserve /usr/local/bin/cryoserve

RUN echo "#!/bin/bash\ncd / && cryo web --port 5000 --host 0.0.0.0" >> cryo.sh \
    && chmod +x cryo.sh

RUN mkdir -p /etc/services.d/cryo_be \
    && mkdir -p /etc/services.d/cryo_fe \
    && echo "#!/command/execlineb -P\nbash /cryo.sh" >> /etc/services.d/cryo_be/run \
    && echo "#!/command/execlineb -P\ncryoserve -port 9091" >> /etc/services.d/cryo_fe/run \
    && chmod +x /etc/services.d/cryo_be/run \
    && chmod +x /etc/services.d/cryo_fe/run

ENTRYPOINT ["/init"]
