"""
Input/Output functions.
"""

import os
import yaml


def read_yaml_from_file(file: str) -> dict:
    """
    Read YAML from file.
    """
    with open(file, 'r') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            raise ValueError("Invalid YAML file") from exc


def write_yaml_to_file(file: str, input: dict) -> None:
    """
    Write YAML to file.
    """
    # Force create directory
    directory = os.path.dirname(file)
    os.makedirs(directory, exist_ok=True)

    with open(file, 'w') as stream:
        try:
            yaml.safe_dump(input, stream, sort_keys=False)
        except yaml.YAMLError as exc:
            raise ValueError("Invalid YAML file") from exc
