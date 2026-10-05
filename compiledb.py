# Include the toolchain headers (newlib, libstdc++, ESP-IDF) in compile_commands.json
# so clangd can resolve <string.h> and friends.
Import("env")

env.Replace(COMPILATIONDB_INCLUDE_TOOLCHAIN=True)
