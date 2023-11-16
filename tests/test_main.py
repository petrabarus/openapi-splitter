import unittest
import os
from openapi_splitter.main import validate_input_file, validate_output_dir

dir_path = os.path.dirname(os.path.abspath(__file__)) + "/"


class TestCommand(unittest.TestCase):
    def test_validate_input_file(self):
        # Test case for when file does not exist
        with self.assertRaises(FileNotFoundError):
            validate_input_file("nonexistent_file.yaml")

        # Test case for when file is not a file
        with self.assertRaises(ValueError):
            validate_input_file(dir_path)

        # Test case for when file is not readable
        with self.assertRaises(ValueError):
            validate_input_file("/usr/bin")

        # Test case for when file is valid
        valid_input_file = dir_path + \
            "/../res/samples/petstore-simple.yaml"
        validate_input_file(valid_input_file)

    def test_validate_output_dir(self):
        # Testcase for when directory does not exist
        with self.assertRaises(FileNotFoundError):
            validate_output_dir("nonexistent_dir")

        # Testcase for when directory is not a directory
        with self.assertRaises(ValueError):
            validate_output_dir(dir_path +
                                "/../res/samples/petstore-simple.yaml")

        # Testcase for when directory is not writable
        with self.assertRaises(ValueError):
            validate_output_dir("/usr/bin")

        # Testcase for when directory is not empty
        with self.assertRaises(ValueError):
            validate_output_dir(dir_path + "/../res/samples")
