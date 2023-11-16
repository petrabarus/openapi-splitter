import argparse
import os

from openapi_splitter.io import read_yaml_from_file, write_yaml_to_file
from openapi_splitter.splitter import Splitter
from openapi_splitter.verbose import vprint


def generate(input_file: str, output_dir: str, verbose=False) -> None:
    """
    Generate the output files.
    """

    input_yaml = read_yaml_from_file(input_file)
    splitter = Splitter(input_yaml, output_dir)
    splitter.split()

    for output_document in splitter.output_documents:
        file_path = output_dir + "/" + output_document.filename
        vprint(verbose, "Writing file: {}".format(file_path))
        write_yaml_to_file(file_path, output_document.yaml)


def validate_input_file(file: str) -> None:
    """
    Validate the input file.

    :param file: The input file.
    """
    if not os.path.exists(file):
        raise FileNotFoundError(f"Input file {file} does not exist.")
    if not os.path.isfile(file):
        raise ValueError(f"Input file {file} is not a file.")
    # Not readable
    if not os.access(file, os.R_OK):
        raise ValueError(f"Input file {file} is not readable.")


def validate_output_dir(dir: str) -> None:
    """
    Validate the output directory.

    :param dir: The output directory.
    """
    # Raise if not exists
    if not os.path.exists(dir):
        raise FileNotFoundError(f"Output directory {dir} does not exist.")
    # Raise if not a directory
    if not os.path.isdir(dir):
        raise ValueError(f"Output directory {dir} is not a directory.")
    # Raise if not writable
    if not os.access(dir, os.W_OK):
        raise ValueError(f"Output directory {dir} is not writable.")
    # Raise if not empty
    if os.listdir(dir):
        raise ValueError(f"Output directory {dir} is not empty.")


def main():
    """
    The main function.
    """
    parser = argparse.ArgumentParser(
        description="Split an OpenAPI specification file into multiple files.")
    parser.add_argument("input_file", help="The input file.")
    parser.add_argument("output_dir", help="The output directory.")
    parser.add_argument("-q",
                        "--quiet",
                        action=argparse.BooleanOptionalAction,
                        help="Quiet mode.")
    args = parser.parse_args()

    try:
        validate_input_file(args.input_file)
        validate_output_dir(args.output_dir)
    except Exception as e:
        print(e)
        parser.print_help()
        exit(1)

    verbose = not args.quiet
    generate(args.input_file, args.output_dir, verbose)


if __name__ == '__main__':
    main()
