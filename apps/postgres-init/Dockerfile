FROM ghcr.io/osnabrugge/alpine:rolling@sha256:69ad27109ef9ca0930715239ecec1ce9ba10a528a7a76750d7c96d48c2c90a41

ARG TARGETPLATFORM
ARG VERSION
ARG CHANNEL

#hadolint ignore=DL3018
RUN apk add --no-cache ca-certificates postgresql14-client~"${VERSION}"

USER kah

COPY ./apps/postgres-init/entrypoint.sh /entrypoint.sh

CMD ["/entrypoint.sh"]

LABEL org.opencontainers.image.source="https://github.com/postgres/postgres"
