# Include the toolchain headers (newlib, libstdc++) in compile_commands.json
# so clangd can resolve <string.h> and friends.
#
# PlatformIO's COMPILATIONDB_INCLUDE_TOOLCHAIN globs every include dir in the
# toolchain package. The esp-14.x toolchain also ships picolibc headers, which
# GCC does not use by default and which break clangd (picolibc's sys/config.h
# shadows newlib's). Ask GCC for its real search path instead, and only when
# generating compile_commands.json, so normal builds are unaffected.
import glob
import os
import subprocess

from SCons.Script import COMMAND_LINE_TARGETS

Import("env")

if "compiledb" in COMMAND_LINE_TARGETS:
    # $CXX is not set yet in a pre: script, so find g++ in the toolchain package.
    mcu = env.BoardConfig().get("build.mcu", "esp32")
    toolchain = env.PioPlatform().get_package_dir("toolchain-xtensa-esp-elf")
    cxx = glob.glob(os.path.join(toolchain, "bin", "xtensa-%s-elf-g++*" % mcu))[0]
    result = subprocess.run(
        [cxx, "-x", "c++", "-E", "-v", "-"],
        input="",
        capture_output=True,
        text=True,
    )
    lines = result.stderr.splitlines()
    start = lines.index("#include <...> search starts here:") + 1
    end = lines.index("End of search list.")
    # -isystem keeps them after the framework's -I dirs, as in a real GCC build
    # (the toolchain has its own xtensa/config/core-isa.h that must not win).
    env.Append(CCFLAGS=["-isystem" + os.path.normpath(line.strip()) for line in lines[start:end]])
