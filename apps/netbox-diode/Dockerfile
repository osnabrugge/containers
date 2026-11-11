# syntax=docker/dockerfile:1
FROM ghcr.io/netbox-community/netbox:v4.7.4@sha256:69cd72d0b0e4928a90940a7011954aaa7060c75fddd8dc6cea2f19407bae45b1

USER root
COPY requirements.lock /tmp/diode-requirements.lock
RUN /usr/local/bin/uv pip install --python /opt/netbox/venv/bin/python --no-cache --require-hashes --requirement /tmp/diode-requirements.lock \
    && /usr/local/bin/uv pip check --python /opt/netbox/venv/bin/python \
    && rm /tmp/diode-requirements.lock

USER ubuntu:ubuntu
