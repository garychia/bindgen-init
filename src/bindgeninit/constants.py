EXAMPLE_HEADER = """#ifndef EXAMPLE_H
#define EXAMPLE_H

int add_numbers(int a, int b);

#endif  // EXAMPLE_H
"""

BUILD_RS = """use std::env;
use std::path::PathBuf;

fn main() {
    // TODO: Specify directories where required shared libraries are located.
    // println!("cargo:rustc-link-search=/path/to/lib");

    // TODO: Link shared libraries.
    // println!("cargo:rustc-link-lib=lib_name");

    // Regenerate the bindings if the wrapper changes
    println!("cargo:rerun-if-changed=example.h");

    // Create bindings
    let bindings = bindgen::Builder::default()
        // The wrapper header file.
        .header("src/example.h")
        // Rebuild the crate if any of the included header files changed.
        .parse_callbacks(Box::new(bindgen::CargoCallbacks))
        .generate()
        .expect("Unable to generate bindings");

    // Write the bindings to $OUT_DIR/bindings.rs.
    let out_path = PathBuf::from(env::var("OUT_DIR").unwrap());
    bindings
        .write_to_file(out_path.join("bindings.rs"))
        .expect("Failed to create bindings!");
}
"""


LIB_RS = """#![allow(non_upper_case_globals)]
#![allow(non_camel_case_types)]
#![allow(non_snake_case)]

include!(concat!(env!("OUT_DIR"), "/bindings.rs"));
"""
