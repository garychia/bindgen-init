import subprocess
import os
from .constants import EXAMPLE_HEADER, BUILD_RS, LIB_RS


def initialize(dest_dir: os.PathLike, project_name: str, bin: bool):
    os.chdir(dest_dir)
    # Create a Cargo project with bindgen installed.
    cargo_command = ["cargo", "new", project_name, "--lib"]
    if bin:
        cargo_command.pop()

    subprocess.run(cargo_command)
    os.chdir(project_name)
    subprocess.run(["cargo", "add", "bindgen", "--build"])

    # Create an example C header file.
    with open("src/example.h", "w") as example_h:
        example_h.write(EXAMPLE_HEADER)

    # Create build.rs file
    with open("build.rs", "w") as build_rs:
        build_rs.write(BUILD_RS)

    # Modify lib.rs file
    with open("src/lib.rs", "w") as lib_rs:
        lib_rs.write(LIB_RS)
