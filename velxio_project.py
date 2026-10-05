# Pack a Velxio project zip (.pio/build/<env>/velxio-project.zip) after every
# build, for Velxio's "Import project": velxio/diagram.json as diagram.json plus
# the sources, with src/main.cpp renamed to sketch.ino.
#
# The root diagram.json stays Wokwi's: Velxio's importer only recognises its own
# `board-velxio-<kind>` part types (frontend/src/utils/wokwiZip.ts), so the board
# needs a separate diagram. Keep both diagrams in sync when adding parts.
import os
import zipfile

Import("env")


def velxio_project(source, target, env):
    project_dir = env.subst("$PROJECT_DIR")
    out = os.path.join(env.subst("$BUILD_DIR"), "velxio-project.zip")
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.write(os.path.join(project_dir, "velxio", "diagram.json"), "diagram.json")
        for folder in ("src", "include"):
            base = os.path.join(project_dir, folder)
            for name in sorted(os.listdir(base)):
                if name.endswith((".ino", ".h", ".hpp", ".c", ".cpp")):
                    arcname = "sketch.ino" if (folder, name) == ("src", "main.cpp") else name
                    zf.write(os.path.join(base, name), arcname)
    print("Velxio project: %s" % out)


env.AddPostAction("$BUILD_DIR/${PROGNAME}.bin", velxio_project)
