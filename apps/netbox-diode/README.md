# NetBox with Diode

The official NetBox image with the compatible Diode plugin installed at build
time. NetBox's entrypoint and default non-root user are preserved.

Enable `netbox_diode_plugin` in NetBox configuration, supply the existing Diode
OAuth credentials through runtime secrets, and run NetBox's normal migrations.
No credentials or deployment-specific configuration are included in this image.

The image version tracks NetBox. Plugin and dependency versions are pinned in
`requirements.lock`; regenerate it from `requirements.txt` with `uv pip compile
--generate-hashes` using the base image's Python.
