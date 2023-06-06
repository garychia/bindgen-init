import argparse
from . import initialize


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("project_name", help="the name of Cargo project")
    parser.add_argument("-b", "--bin", action="store_true", help="(Optional) generate a Cargo binary project instead of a library project")
    args = parser.parse_args()

    project_name = args.project_name

    initialize(".", project_name, args.bin)
    print("Cargo bindgen project created successfully!")


if __name__ == "__main__":
    main()
