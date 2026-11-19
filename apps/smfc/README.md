# SMFC with a fresh-temperature alternative

This image retains the pinned official SMFC 6.5.0 runtime and changes only its
hard-disk temperature reader. If an existing HWMON file returns an I/O error,
it tries a fresh `smartctl -A -j` temperature with a five-second subprocess
timeout. Valid hot readings remain hot; unavailable or invalid alternatives
still enter SMFC's original error handling and fail-high behavior.

The change does not unload the host's `drivetemp` module, drop monitored devices,
extend cached-temperature tolerance, change fan curves or suppress emergency
100% duty. SMART reads can wake a sleeping disk.

The original GPL-3.0 license is retained. The complete upstream source is
[SMFC 6.5.0](https://github.com/petersulyok/smfc/tree/dd14211f1a7369a919a11c895a0aa0d9a1bb433a);
the downstream source change is [hwmon.patch](./hwmon.patch).

Container tests substitute file and process I/O. They require no IPMI device,
disk access or elevated container privileges.
