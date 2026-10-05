# PlatformIO Wokwi ESP32

A reusable ESP32 DevKit starter project for PlatformIO and Wokwi.

Use this repository as a base for ESP32 projects that need local development with PlatformIO and circuit simulation with Wokwi.

## Included

- PlatformIO configuration for the ESP32 DevKit (`esp32dev`)
- Arduino framework, serial monitor at 115200 baud
- Wokwi simulation with an ESP32 DevKit C v4 wired to the serial monitor
- Zed tasks and clangd setup
- `mise.toml` with pinned `pio` and `wokwi-cli`
- Standard PlatformIO project structure

## Getting started

This project works best in conjunction with [Visual Studio Code](https://code.visualstudio.com/), [PlatformIO IDE](https://marketplace.visualstudio.com/items?itemName=platformio.platformio-ide), and [Wokwi Simulator for VS Code](https://marketplace.visualstudio.com/items?itemName=Wokwi.wokwi-vscode).

Install the tools before opening the project:

1. [Install Visual Studio Code](https://code.visualstudio.com/download)
2. [Install PlatformIO IDE in VS Code](https://marketplace.visualstudio.com/items?itemName=platformio.platformio-ide)
3. [Install Wokwi Simulator in VS Code](https://marketplace.visualstudio.com/items?itemName=Wokwi.wokwi-vscode)

Clone this repository and open it in VS Code.

### Using Zed

The project also works in [Zed](https://zed.dev/) through the [PlatformIO Core CLI](https://docs.platformio.org/en/latest/core/installation/index.html) (`pio`) and, optionally, the [Wokwi CLI](https://docs.wokwi.com/wokwi-ci/cli-installation) (`wokwi-cli`, needs a `WOKWI_CLI_TOKEN`).

1. Install PlatformIO Core and make sure `pio` is on your `PATH`, or run `mise install` to get `pio` and `wokwi-cli` from `mise.toml` with [mise](https://mise.jdx.dev/)
2. Open the folder in Zed
3. Run `task: spawn` (`alt-shift-t`) and pick a task from `.zed/tasks.json`:
   - `PlatformIO: Build`, `Upload`, `Upload and Monitor`, `Serial Monitor`, `Clean`, `Test`
   - `PlatformIO: Generate compile_commands.json (clangd)`
   - `Wokwi: Simulate` (build first)
4. Run the `compile_commands.json` task once (and again after changing `platformio.ini` or libraries) so clangd can resolve `Arduino.h` and the ESP32 headers. `.clangd` removes GCC-only Xtensa flags that clang does not understand.

Build the project with:

```bash
pio run
```

The first build downloads the ESP32 toolchain and Arduino core, so it takes a while.

The Wokwi configuration uses the PlatformIO build output:

- Firmware: `.pio/build/esp32dev/firmware.bin`
- ELF: `.pio/build/esp32dev/firmware.elf`

Edit `src/main.cpp` to add your application code and `diagram.json` to add components and wiring for your simulation.

## Project structure

```
.
├── diagram.json      # Wokwi circuit definition
├── platformio.ini    # PlatformIO configuration
├── mise.toml         # Dev tools (pio, wokwi-cli) for mise
├── wokwi.toml        # Wokwi simulation configuration
├── compiledb.py      # Adds toolchain headers to compile_commands.json
├── .clangd           # clangd settings for Zed
├── .zed/             # Zed tasks and project settings
├── src/
│   └── main.cpp      # Application entry point
├── include/          # Project headers
├── lib/              # Project libraries
└── test/             # PlatformIO tests
```

## License

[MIT](LICENSE)
