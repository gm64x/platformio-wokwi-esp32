# Project scripts

This directory keeps the project's PlatformIO helper scripts and filesystem upload wrappers together.

| Script | Purpose |
| --- | --- |
| `compiledb.py` | Adds toolchain headers to `compile_commands.json` for clangd. |
| `merge_firmware.py` | Combines the ESP32 bootloader, partition table and app into the full flash image used by Velxio. |
| `port_select.py` | Adds `pio run -t select_port` and stores the selected port in the ignored `port.local.ini`. |
| `upload-filesystem.sh` | Linux wrapper for `pio run -t uploadfs`. |
| `upload-filesystem.ps1` | Windows PowerShell wrapper for `pio run -t uploadfs`. |

The upload wrappers change to the project root before running PlatformIO, so they can be launched from another working directory. The `upload-fs` task in `mise.toml` selects the Bash wrapper on Linux and the PowerShell wrapper on Windows. Zed and VS Code expose the same `build-fs` and `upload-fs` mise tasks.

To build the image without uploading it, use `mise run build-fs`. To build and upload it, use `mise run upload-fs`, or run the platform-specific wrapper directly:

```sh
bash scripts/upload-filesystem.sh
```

```powershell
.\scripts\upload-filesystem.ps1
```

These scripts upload the LittleFS image to the ESP32; mounting the filesystem happens in the Arduino firmware with `LittleFS.begin()`. See [`../data/README.md`](../data/README.md) for filesystem contents and runtime access.
