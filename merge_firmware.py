# Merge bootloader, partition table, boot_app0 and app into one flash image
# (.pio/build/<env>/firmware.merged.bin) after every build.
#
# Velxio runs ESP32 firmware in QEMU, which boots from a complete flash image
# (2/4/8/16 MB, DIO), not from the app-only firmware.bin. Same recipe as the
# Velxio docs: https://github.com/davidmonterocrespo24/velxio/blob/master/docs/ESP32_EMULATION.md
#
# pioarduino ships esptool v5, which renamed merge_bin and its flags
# (merge-bin, --flash-mode, --flash-size, --pad-to-size). The platform also
# writes firmware.factory.bin, but it is not padded to the full flash size.
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
                "merge-bin",
                "-o", '"$BUILD_DIR/${PROGNAME}.merged.bin"',
                "--flash-mode", "dio",
                "--flash-size", flash_size,
                "--pad-to-size", flash_size,
            ]
            + ['"%s"' % i for i in images]
        )
    )


env.AddPostAction("$BUILD_DIR/${PROGNAME}.bin", merge_firmware)
