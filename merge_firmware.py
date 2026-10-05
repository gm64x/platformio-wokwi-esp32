# Merge bootloader, partition table, boot_app0 and app into one flash image
# (.pio/build/<env>/firmware.merged.bin) after every build.
#
# Velxio runs ESP32 firmware in QEMU, which boots from a complete flash image
# (2/4/8/16 MB, DIO), not from the app-only firmware.bin. Same recipe as the
# Velxio docs: https://github.com/davidmonterocrespo24/velxio/blob/master/docs/ESP32_EMULATION.md
Import("env")


def merge_firmware(source, target, env):
    flash_size = env.BoardConfig().get("upload.flash_size", "4MB")
    images = []
    for offset, image in env.get("FLASH_EXTRA_IMAGES", []):
        images += [offset, env.subst(image)]
    images += [env.subst("$ESP32_APP_OFFSET"), str(target[0])]

    env.Execute(
        " ".join(
            [
                '"$PYTHONEXE"',
                '"$OBJCOPY"',
                "--chip", env.BoardConfig().get("build.mcu", "esp32"),
                "merge_bin",
                "-o", '"$BUILD_DIR/${PROGNAME}.merged.bin"',
                "--flash_mode", "dio",
                "--flash_size", flash_size,
                "--fill-flash-size", flash_size,
            ]
            + ['"%s"' % i for i in images]
        )
    )


env.AddPostAction("$BUILD_DIR/${PROGNAME}.bin", merge_firmware)
