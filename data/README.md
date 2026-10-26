# Filesystem data

PlatformIO uses this directory as the source for the ESP32 filesystem image. In this project, `platformio.ini` sets `board_build.filesystem = littlefs`, so files placed here are packaged as a LittleFS filesystem, separate from the application firmware.

## What belongs here

Use `data/` for files the firmware needs to read at runtime, for example:

- Web interface assets served by `ESPAsyncWebServer`: HTML, CSS, JavaScript, icons and images
- JSON, text or CSV files containing defaults, templates, lookup tables or other static content
- Binary assets such as fonts, certificates or small models, when the application needs file-style access to them

Keep C/C++ source and headers in `src/`, `include/` or `lib/`, not here. For a few small, frequently updated key-value settings, the ESP32 `Preferences` (NVS) API is usually a better fit than files. Use LittleFS when the data is naturally file-based or larger.

Example layout:

```text
data/
├── index.html
├── css/
│   └── app.css
├── js/
│   └── app.js
└── config/
    └── defaults.json
```

The paths inside the filesystem retain this directory structure. For example, `data/config/defaults.json` is opened by firmware as `/config/defaults.json`.

## Build and upload

From the project root, run:

```sh
pio run -t buildfs
pio run -t uploadfs
```

`buildfs` creates the filesystem image from the contents of `data/`; `uploadfs` sends that image to the board's filesystem partition. A normal `pio run` builds the firmware, and `pio run -t upload` uploads the firmware; neither command by itself uploads changed files from `data/`.

The same two operations are available as editor and mise tasks:

| Operation | Zed / VS Code | mise |
| --- | --- | --- |
| Build image only | `PlatformIO: Build Filesystem Image` | `mise run build-fs` |
| Build and upload image | `PlatformIO: Upload Filesystem Image` | `mise run upload-fs` |

In VS Code, open the Command Palette and choose **Tasks: Run Task**. In Zed, run `task: spawn` and select the task. The `uploadfs` task creates or refreshes the image before uploading it.

After uploading, the Arduino firmware must mount LittleFS and open the files. For example:

```cpp
#include <LittleFS.h>

void setup() {
  Serial.begin(115200);

  if (!LittleFS.begin()) {
    Serial.println("Could not mount LittleFS");
    return;
  }

  File file = LittleFS.open("/config/defaults.json", "r");
  if (!file) {
    Serial.println("Could not open defaults.json");
    return;
  }

  Serial.println(file.readString());
  file.close();
}
```

Avoid `LittleFS.begin(true)` unless formatting on mount failure is intentional: it can erase existing filesystem contents when mounting fails.

## Notes

- `board_build.filesystem = littlefs` selects the filesystem format; it does **not** set the filesystem partition's size. This project does not currently set `board_build.partitions`, so PlatformIO uses the board/framework default partition table. Review that table or define a custom one if the application needs a different allocation.
- Every file in `data/` is included in the filesystem image. That includes this `README.md`, which will appear on the device as `/README.md`. Move documentation outside `data/` if it should not be shipped, or arrange a custom filtering step before building the image.
- Uploading a new filesystem image replaces the filesystem partition and can erase files written by the device at runtime. Keep source assets here; do not treat this upload as a safe way to update firmware while preserving user data.
- Do not put secrets in this directory. Files in flash are not protected merely because they are stored in LittleFS.
- The current `data/` directory is only documentation; the application does not yet mount or use LittleFS.

## References

- [PlatformIO: Uploading files to the ESP32 filesystem](https://docs.platformio.org/en/latest/platforms/espressif32.html#uploading-files-to-file-system)
- [PlatformIO: `data_dir` project option](https://docs.platformio.org/en/latest/projectconf/sections/platformio/options/directory/data_dir.html)
- [ESP-IDF: Filesystem considerations](https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-guides/file-system-considerations.html)
- [Arduino-ESP32: Preferences](https://docs.espressif.com/projects/arduino-esp32/en/latest/api/preferences.html)
