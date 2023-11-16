"""

"""

import unittest
import os
from dataclasses import dataclass
import tempfile
from openapi_splitter.io import read_yaml_from_file, write_yaml_to_file


dir_path = os.path.dirname(os.path.abspath(__file__)) + "/"


class TestIO(unittest.TestCase):
    def test_read_yaml_from_file(self):

        @dataclass
        class TestCase:
            name: str
            input_file: str
            expect_exception: bool = False

        test_cases = [
            TestCase("test 1", "../res/samples/api-with-example.yaml"),
            TestCase("test 2", "../res/samples/petstore-expanded.yaml"),
            TestCase("test_1", "../res/samples/petstore-simple.yaml"),
            TestCase("test_2", "../res/samples/petstore.yaml"),
            TestCase("test_3", "../res/samples/uspto.yaml", True),
        ]

        for test_case in test_cases:
            file_path = dir_path + test_case.input_file
            if test_case.expect_exception:
                with self.assertRaises(Exception):
                    read_yaml_from_file(file_path)
            else:
                actual = read_yaml_from_file(file_path)
                self.assertTrue(
                                isinstance(actual, dict),
                                "failed {}".format(test_case.name))
                # print(actual)

    def test_write_yaml_to_file(self):
        test_file = dir_path + "../res/samples/api-with-example.yaml"
        yaml = read_yaml_from_file(test_file)
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp:
            write_yaml_to_file(temp.name, yaml)
            new_yaml = read_yaml_from_file(temp.name)
            self.assertTrue(isinstance(new_yaml, dict))
