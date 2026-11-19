# syntax=docker/dockerfile:1
FROM docker.io/petersulyok/smfc:6.5.0@sha256:2256941cedd39cf3832ccc95dbd1dacfff76ca83b074aceab43c3e80822ae9ac AS upstream

FROM docker.io/library/alpine:3.24@sha256:f59abe656b692d901e184be3445e084786602108599d2a51d229c0f5a48c71bf AS patched
RUN apk add --no-cache patch
COPY --from=upstream /usr/lib/python3.14/site-packages/smfc/hdfc.py /patched/src/smfc/hdfc.py
COPY hwmon.patch /patched/hwmon.patch
RUN patch --batch --forward --fuzz=0 -p1 -d /patched < /patched/hwmon.patch

FROM upstream
COPY --from=patched /patched/src/smfc/hdfc.py /usr/lib/python3.14/site-packages/smfc/hdfc.py
ADD --checksum=sha256:3972dc9744f6499f0f9b2dbf76696f2ae7ad8af9b23dde66d6af86c9dfb36986 https://raw.githubusercontent.com/petersulyok/smfc/dd14211f1a7369a919a11c895a0aa0d9a1bb433a/LICENSE /usr/share/licenses/smfc/LICENSE
