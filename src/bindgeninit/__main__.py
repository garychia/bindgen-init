import subprocess
import os
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("project_name", help="the name of Cargo project")
    parser.add_argument("-b", "--bin", action="store_true", help="(Optional) generate a Cargo binary project instead of a library project")
    args = parser.parse_args()

    project_name = args.project_name

    # Create a Cargo project with bindgen installed.
    cargo_command = ["cargo", "new", project_name, "--lib"]
    if args.bin:
        cargo_command.pop()

    subprocess.run(cargo_command)
    os.chdir(project_name)
    subprocess.run(["cargo", "add", "bindgen", "--build"])

    # Create an example C header file.
    with open("src/example.h", "w") as example_h:
        example_h.write('#ifndef EXAMPLE_H\n')
        example_h.write('#define EXAMPLE_H\n\n')
        example_h.write('int add_numbers(int a, int b);\n\n')
        example_h.write('#endif  // EXAMPLE_H\n')


    # Create build.rs file
    with open("build.rs", "w") as build_rs:
        build_rs.write('use std::env;\n')
        build_rs.write('use std::path::PathBuf;\n\n')
        build_rs.write('fn main() {\n')
        build_rs.write('    // TODO: Specify directories where required shared libraries are located.\n')
        build_rs.write('    // println!("cargo:rustc-link-search=/path/to/lib");\n\n')
        build_rs.write('    // TODO: Link shared libraries.\n')
        build_rs.write('    // println!("cargo:rustc-link-lib=lib_name");\n\n')
        build_rs.write('    // Regenerate the bindings if the wrapper changes\n')
        build_rs.write('    println!("cargo:rerun-if-changed=example.h");\n\n')
        build_rs.write('    // Create bindings\n')
        build_rs.write('    let bindings = bindgen::Builder::default()\n')
        build_rs.write('        // The wrapper header file.\n')
        build_rs.write('        .header("src/example.h")\n')
        build_rs.write('        // Rebuild the crate if any of the included header files changed.\n')
        build_rs.write('        .parse_callbacks(Box::new(bindgen::CargoCallbacks))\n')
        build_rs.write('        .generate()\n')
        build_rs.write('        .expect("Unable to generate bindings");\n\n')
        build_rs.write('    // Write the bindings to $OUT_DIR/bindings.rs.\n')
        build_rs.write('    let out_path = PathBuf::from(env::var("OUT_DIR").unwrap());\n')
        build_rs.write('    bindings\n')
        build_rs.write('        .write_to_file(out_path.join("bindings.rs"))\n')
        build_rs.write('        .expect("Failed to create bindings!");\n')
        build_rs.write('}\n')

    # Modify lib.rs file
    with open("src/lib.rs", "w") as lib_rs:
        lib_rs.write('#![allow(non_upper_case_globals)]\n')
        lib_rs.write('#![allow(non_camel_case_types)]\n')
        lib_rs.write('#![allow(non_snake_case)]\n\n')
        lib_rs.write('include!(concat!(env!("OUT_DIR"), "/bindings.rs"));\n')

    print("Cargo bindgen project created successfully!")


if __name__ == "__main__":
    main()
