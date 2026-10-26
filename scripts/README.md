# Project helper scripts

This directory contains project-level scripts used by PlatformIO and the simulator tooling.

| Script | Purpose |
| --- | --- |
| `compiledb.py` | Adds toolchain headers to `compile_commands.json` so clangd can resolve ESP32 and standard library headers. |
| `merge_firmware.py` | Combines the bootloader, partition table, `boot_app0` and application into the full flash image used by Velxio. |
| `port_select.py` | Adds `pio run -t select_port` and stores the selected serial port in the git-ignored `port.local.ini`. |

`platformio.ini` references the PlatformIO hooks in this directory. Keep additional project scripts here and reference them from the appropriate tool configuration.
