# Project scripts

This directory contains the project's PlatformIO hooks and the cross-platform LittleFS uploader.

| Script | Purpose |
| --- | --- |
| `compiledb.py` | Adds toolchain headers to `compile_commands.json` so clangd can resolve ESP32 and standard library headers. |
| `merge_firmware.py` | Combines the bootloader, partition table, `boot_app0` and application into the full flash image used by Velxio. |
| `port_select.py` | Adds `pio run -t select_port` and stores the selected serial port in the git-ignored `port.local.ini`. |
| `upload-filesystem.sh` | Linux wrapper for `pio run -t uploadfs`. |
| `upload-filesystem.ps1` | Windows PowerShell wrapper for `pio run -t uploadfs`. |

`platformio.ini` references the PlatformIO hooks in this directory. The upload wrappers change to the project root before running PlatformIO, so they can be launched from another working directory. The `upload-fs` task in `mise.toml` selects the Bash wrapper on Linux and the PowerShell wrapper on Windows. Zed and VS Code expose the same `build-fs` and `upload-fs` mise tasks.

To build the LittleFS image without uploading it, use `mise run build-fs`. To build and upload it, use `mise run upload-fs`, or call the platform-specific wrapper directly:

```sh
bash scripts/upload-filesystem.sh
```

```powershell
.\scripts\upload-filesystem.ps1
```

These scripts upload the LittleFS image to the ESP32; mounting the filesystem happens in the Arduino firmware with `LittleFS.begin()`. See [`../data/README.md`](../data/README.md) for filesystem contents and runtime access.

## Test the upload wrappers

The wrapper tests replace `pio` with a temporary stub, so they verify the working directory, arguments and exit-code propagation without requiring a board or writing flash. Run the relevant test from the project root:

```sh
bash scripts/tests/test-upload-filesystem.sh
```

```powershell
.\scripts\tests\test-upload-filesystem.ps1
```

The GitHub Actions workflow in `.github/workflows/script-tests.yml` runs the Bash test on Ubuntu and the PowerShell test on Windows.
