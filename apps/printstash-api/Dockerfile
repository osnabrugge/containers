# syntax=docker/dockerfile:1
FROM ghcr.io/xiao-villamor/printstash-api:v0.15.1@sha256:ce7261a7722d52ce499e442e7adc120d1429b80ca7ec90d927b5f8614841d64c AS upstream

FROM docker.io/library/alpine:3.24@sha256:f59abe656b692d901e184be3445e084786602108599d2a51d229c0f5a48c71bf AS patched
RUN apk add --no-cache patch
COPY --from=upstream /app/app/modules/ingestion /patched/app/modules/ingestion
COPY capture.patch /patched/capture.patch
RUN patch --batch --forward --fuzz=0 -p1 -d /patched < /patched/capture.patch
ADD --checksum=sha256:8d56b405468aad11f87ab5763f901e276e08d9646ff5c8481b1762b6b789e9ed https://raw.githubusercontent.com/xiao-villamor/PrintStash/b45b65d0c7d4faca5856da37187f893ba0662596/LICENSE /licenses/printstash/LICENSE

FROM upstream
COPY --from=patched /patched/app/modules/ingestion/inbox.py /patched/app/modules/ingestion/staging_leases.py /app/app/modules/ingestion/
COPY --from=patched /licenses/printstash/LICENSE /usr/share/licenses/printstash/LICENSE
